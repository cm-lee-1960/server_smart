from datetime import datetime
from tkinter.simpledialog import SimpleDialog
from django.conf import settings
from django.db.models import Q
from monitor.models import Phone, MeasureCallData, Message
from management.models import MeasureingTeam, ReportCycle
from monitor.geo import make_map_locations

#--------------------------------------------------------------------------------------------------
# 두개의 측정 단말기의 콜 가운트가 동일하고, 메시지 전송기준 콜 수 있지 확인한다.
# 2022.02.25 - 측정 단말기의 총 콜카운트가 아닌 측정 데이터의 현재 콜카운트를 기준으로 메시지 전송여부를 판단한다.
#              단, 측정시작은 현재 콜카운트가 누락될 수 있으니 측정단말의 총 콜카운트가 1일 때로 판단한다.
# 2022.02.27 - 측정시작 메시지 조건 분리 반영
#            - 통신사, 측정유형에 상관없이 측정시작을 판단한다.
#            *** [해결해야할 잠재이슈] 단말 하나로 측정을 하는 경우 주기적인 메시지 전송 판단처리 고민 필요
# 2022.03.04 - 측정 보고주기를 데이터베이스에 등록하여 관리하도록 코드를 수정함 (측정 보고주기 확인 : ReportCycle)
# 2022.03.10 - 측정 보고주기 판단기준을 현재 콜카운트에서 측정 단말기의 측정 데이터 건수(total_count)로 변경
# 2022.03.11 - 측정시작 메시지 분리
#              1) 전체대상 측정시작 메시지(START_F)
#              2) 해당지역 측정시작 메시지(START_M)
# 2022.03.12 - 측정시작 위치와 현재 측정위치의 거리가 1km 이상 떨어졌을 때 지도가 자동축소 되도록 함
#--------------------------------------------------------------------------------------------------
def current_count_check(mdata):
    """DL/UL 측정단말의 현재 콜카운트와 보고기준 콜카운트를 확인한다."""
    result = False
    phone = mdata.phone
    # 해당지역에 단말이 첫번째로 측정을 시작했는지 확인한다.
    # print("current_count_check()-total_count", phone.total_count)
    if mdata.currentCount == 1:
        # # 해당일자에 첫번째 측정 단말기일 경우, 측정시작 메시지를 전송한다. 
        # # 즉, 해당일자에 측정중인 단말이 없다면 메시지를 전송한다.
        # qs = Phone.objects.filter(measdate=phone.measdate, manage=True).exclude(phone_no=phone.phone_no)
        # if not qs.exists():
        #     result = True
        # 측정시작 조건 : 현재 콜카운트가 1인 다른 측정 데이터가 있는지 확인
        # - 결과 <= 1건 : 자기 자신밖에 없으니 측정시작 메시지 전송
        # - 결과 > 1건 : 이미 측정시작 메시지를 전송했으니 메시지를 전송하지 않음
        # 2022.03.11 - 1)전체대상 측정시작 메시지(START_F)
        meastime_from = int(str(mdata.meastime)[:8] + '000000000') # 조회시작
        meastime_to = int(str(mdata.meastime)[:8] + '235959999') # 조회종료
        qs = MeasureCallData.objects.filter(Q(meastime__gte=meastime_from) & Q(meastime__lte=meastime_to))
        if mdata.phone.status == 'START_F' and len(qs) <= 1:
            result = True
        
        # 2022.03.11 - 2)해당지역 측정시작 메시지(START_M)
        # 2-1) 상대편 측정 단말기가 등록되어 있는지 확인한다. 
        # 2-2) 상대편 측정 단말기에 속도 측정 데이터가 있는지 확인한다.
        elif mdata.phone.status == 'START_M' and mdata.phone.manage == True:
            qs = mdata.phone.phoneGroup.phone_set.exclude(phone_no=mdata.phone_no)
            if qs.exists():
                oPhone = qs[0]
                qs = oPhone.measurecalldata_set.filter(currentCount=1, testNetworkType='speed')
                if not qs.exists():
                    result = True

    # elif mdata.currentCount in [3, 10, 27, 37, 57,]:
    # 2022.03.10 currentCount -> phone.total_count로 변경 적용
    elif phone.total_count in [ int(x) for x in ReportCycle.objects.all()[0].reportCycle.split(',')]:
        # 단말기 체인지 되고 재측정시 그데이터도 더해져서 메시지가 보내질수도 있다 그때는 예외조건
        # 단밀기 그룹으로 묶여 았는 상대편 측정 단말기를 조회한다.
        qs = phone.phoneGroup.phone_set.exclude(phone_no=phone.phone_no)
        if qs.exists():
            p = qs[0]
            # 상대편 측정 단말기의 현재 콜 카운트가 측정 단말 보다 같거나 커야 한다.
            if p.total_count >= phone.total_count:
                result = True
        # 2022.02.26 - 측정단말이 하나인 경우 어떻게 처리해야 할지 고민이 필요하다.
        # 2022.03.05 - 속도측정의 경우 대부분 2대의 측정 단말기를 가지고 진행을 하며, 최소한 3콜 이전에는 2대 모두의 측정 데이터가
        #              발생한다는 가정으로 진행함
        #              즉, 3콜에도 상대편 단말기의 측정 데이터가 없으면 1개의 측정 단말기로 측정을 진행한다고 생각하고,
        #              보고주기에 따라 메시지를 보냄
        # Case 1 : 1,2,3,4,5,...27,1,2,3,4,5,..27,.. (DL을 측정하고, 이후 UL을 측정하는 경우)
        # Case 1 : 1,1,2,2,3,3,4,4,5,5,6,6,...27,27,.. (DL과 UL을 번갈아 한번씩 측정하는 경우)
        else:
            pass
            # 2022.03.10 currentCount -> phone.total_count로 변경 적용하면서 추가 고민해야 함
            # qs = MeasureCallData.objects.filter(phone_no=mdata.phone_no, currentCount__lte=mdata.currentCount)
            # if qs.exists() and qs.count() > mdata.currentCount:
            #    qs = qs.filter(currentCount = mdata.currentCount)
            #    if qs.count() > 1:
            #         result = True
            # else:
            #     result = True

    return result

#--------------------------------------------------------------------------------------------------
# 측정 단말기의 상태에 따라서 전송 메시지를 생성한다.
# 2022.02.27 - 측정 단말기 Power-On/Off 데이터를 별도로 추가 받아야 한다고 함
# 2022.03.05 - 메시지 내용 중에서 숫자에 자동으로 링크가 붙는 것을 조치함 (앞뒤에 <code></code>를 붙임)
#--------------------------------------------------------------------------------------------------
def make_message(mdata):
    """측정단말의 상태에 따라서 메시지를 작성한다."""

    # 환경변수에서 채팅방 채널IF를 가져온다.
    # channelId = '-736183270'
    channelId = settings.CHANNEL_ID

    phone = mdata.phone
    status = ["POWERON", "START_F", "START_M", "MEASURING", "END"]
    # 측정 진행 메시지는 DL/UP 측정 단말기의 현재 콜 카운트가 같고, 3, 10, 27, 37, 57 콜 단위로 보고함
    if phone.status in status and current_count_check(mdata):
        # 측정 단말기의 DL/UP 평균값들을 가져온다.
        dl_sum, ul_sum, dl_count, ul_count = 0, 0, 0, 0
        dl_nr_count, ul_nr_count = 0, 0 # 5G->LTE 전환콜수(DL, UL)ß
        avg_downloadBandwidth = 0  # 다운로드 평균속도
        avg_uploadBandwidth = 0  # 업로드 평균속도
        # nr_count = 0 # 5G->NR 전환 콜수
   

        # 2022.02.26 - 데이터가 맞지 않아 재작성 함
        #            - 속도평균값을 산출할 때 고민해야 하는 사항은 몇번째 턴인지, 현재 콜카운트, 총 측정횟수 등을 고려해야 한다.
        #                       <--- tern 1 ----> <--- tern 2 --->
        #            - Phone 1: 1,2,3,4,5,6,...27,1,2,3,4,5,...
        #              Phone 2: 1,  3,4,5,6,...27,1,2,3,  5,... * 콜이 누락되는 경우도 있음
        #            - tern : 현재 콜카운트가 증가하다 감소하면 한개의 턴(측정주기, tern)이 끝난 것으로 판단
        #                     즉, 현재 콜카운트가 3이라면 첫번째 측정주기의 3번째 콜인지? 두번째 측정주기의 3번째 콜인지? 확인해서
        #                     상대편 측정단말의 속도평균을 산출할때 동일한 기준을 적용해야 한다.   
        #
        # 2022.03.10 currentCount -> phone.total_count로 변경 적용
        # 메시지를 보내려고 하는 측정 단말기
        total_count = 0
        for m in phone.measurecalldata_set.filter(testNetworkType='speed').order_by("meastime"):
            if total_count >= phone.total_count: break
            if m.phone.networkId == '5G' and m.networkId == 'NR':
                # 측정 단말이 5G이고, 측정 데이터가 NR이면 5G->NR 전환 콜수를 하나 증가시킨다. 
                if m.downloadBandwidth and m.downloadBandwidth > 0:
                    dl_nr_count += 1
                if m.uploadBandwidth and m.uploadBandwidth > 0:
                    ul_nr_count += 1
            else: 
                # 속도 평균값을 구하기 위한 속도 합계와 콜 카운트를 누적한다. 
                if m.downloadBandwidth and m.downloadBandwidth > 0:
                    dl_sum +=  m.downloadBandwidth
                    dl_count += 1
                if m.uploadBandwidth and m.uploadBandwidth > 0:
                        ul_sum += m.uploadBandwidth
                        ul_count += 1
            # 5G->LTE 전환포함하여 콜 카운트를 산정한다.
            total_count += 1
            # print(f"###-1 {phone.phone_no}/{m.currentCount}/{m.downloadBandwidth}/{m.uploadBandwidth }///", mdata.currentCount)
           
        # 상대편 측정 단말기
        total_count = 0
        qs = phone.phoneGroup.phone_set.filter(ispId='45008', manage=True).exclude(phone_no=phone.phone_no)
        if qs.exists():
            oPhone = qs[0]
            for m in oPhone.measurecalldata_set.filter(testNetworkType='speed').order_by("meastime"):
                # 2022.02.25 DL/UL 측정건수가 10건 이상 차이가 나지 않는다는 가정에서 아래 코드가 정상 동작한다.
                if total_count >= phone.total_count: break
                if m.phone.networkId == '5G' and m.networkId == 'NR':
                    # 측정 단말이 5G이고, 측정 데이터가 NR이면 5G->NR 전환 콜수를 하나 증가시킨다. 
                    if m.downloadBandwidth and m.downloadBandwidth > 0:
                        dl_nr_count += 1
                    if m.uploadBandwidth and m.uploadBandwidth > 0:
                        ul_nr_count += 1
                else: 
                    # 속도 평균값을 구하기 위한 속도 합계와 콜 카운트를 누적한다. 
                    if m.downloadBandwidth and m.downloadBandwidth > 0:
                        dl_sum +=  m.downloadBandwidth
                        dl_count += 1
                    if m.uploadBandwidth and m.uploadBandwidth > 0:
                            ul_sum += m.uploadBandwidth
                            ul_count += 1
                # 5G->LTE 전환포함하여 콜 카운트를 산정한다.
                total_count += 1
                # print(f"###-2 {oPhone.phone_no}/{m.currentCount}/{m.downloadBandwidth}/{m.uploadBandwidth }///", mdata.currentCount)

        # DL/UL 평균속도를 산출한다.         
        if dl_count > 0 : avg_downloadBandwidth = round(dl_sum / dl_count,2)
        if ul_count > 0 : avg_uploadBandwidth = round(ul_sum / ul_count,2)
        # if nr_count > 0 : avg_nrRate = round(nr_count / (dl_count + ul_count) * 100,2)

        # 메시지를 작성한다.
        #                01234567890123456
        # last_updated : 20211101235959999
        last_updated_str = str(mdata.phone.last_updated)
        mmdd = last_updated_str[4:6] + "." + str(int(last_updated_str[6:8]))
        hhmm = last_updated_str[8:10] + ":" + last_updated_str[10:12]
        # [파워온 메시지] -------------------------------------------------------------------------------------
        POWERON_MSG = f"{mdata.userInfo1}에서 단말이 켜졌습니다."
        # [측정시작 메시지] -----------------------------------------------------------------------------------
        # 당일 측정조 메시지 내용을 가져온다.
        
        if phone.status == 'START_F':
            measuringteam_msg = '' # 당일 측정조 (데이터베이스에서 가져와야 함)
            meastime_str = str(mdata.meastime)
            measdate = datetime.strptime(meastime_str[:8], "%Y%m%d")
            qs = MeasureingTeam.objects.filter(measdate=measdate)
            if qs.exists(): 
                measuringteam_msg = qs[0].message
            messages = f"금일({mmdd}일) S-CXI 품질측정이 {hhmm}분에 {mdata.get_address()}에서 시작되었습니다.\n" + \
                       f"{measuringteam_msg}\n" + \
                        "\n평가에 만전을 기하여 주시기 바랍니다. "
        elif phone.status == 'START_M':
            messages = f"S-CXI {mdata.phone.morphology} {mdata.get_address()} 측정시작({mdata.get_time()}~)"

        # [측정진행 메시지] -----------------------------------------------------------------------------------
        elif phone.status == 'MEASURING':
            # WiFi 측정 데이터의 경우
            if phone.networkId == 'WiFi':
                messages = f"<code>{mdata.get_address()} 현재 콜카운트 {phone.total_count}번째 측정중입니다.\n" + \
                            "속도(DL/UL, Mbps)\n" + \
                            f"{phone.networkId}(상용): {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}</code>"
            # 5G 측정 데이터의 경우
            elif phone.networkId == '5G':
                messages = f"<code>{phone.networkId} {mdata.get_address()} 측정({phone.starttime}~, {phone.total_count}콜 진행중)\n" + \
                            f"- LTE 전환(DL/UL, 콜): {dl_nr_count}/{ul_nr_count}\n" + \
                            f"- 속도(DL/UL, Mbps): {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}</code>"
            # 기타(LTE, 3G) 측정데이터의 경우
            else:
                messages = f"<code>{phone.networkId} {mdata.get_address()} 측정({phone.starttime}~, {phone.total_count}콜 진행중)\n" + \
                            f"- 속도(DL/UL, Mbps): {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}</code>"
        
        # [측정종료 메시지] -----------------------------------------------------------------------------------
        # 2022-03-11 - 측정종료 메시지는 수기로 해당지역 측정종료 및 당일 측정종료를 실행할 때 생성되기 때문에 여기에 있는 코드를 사용하지 않음
        elif phone.status == 'END':
            messages = f"<code>금일({mmdd}일) S-CXI 품질측정이 {hhmm}분에 {mdata.userInfo1}을 마지막으로 종료 되었습니다.\n" + \
                        "(DL/UL/시도호/성공률)\n" + \
                        f"{phone.networkId}: {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}/{dl_count+ul_count}/-</code>"


        # 해당 측정위치에 대한 지도맵을 작성하고, 메시지 하단에 [지도보기] 링크를 붙인다.
        filename = make_map_locations(mdata)
        messages += f"\n<a href='http://127.0.0.1:8000/monitor/maps/{filename}'>지도보기</a>"

        # 전송 메시지를 생성한다.
        Message.objects.create(
            phone=phone,
            measdate=str(mdata.meastime)[0:8],
            sendType='TELE',
            userInfo1=mdata.userInfo1,
            currentCount=mdata.currentCount,
            phone_no=mdata.phone_no,
            downloadBandwidth=avg_downloadBandwidth,
            uploadBandwidth=avg_uploadBandwidth,
            messageType='SMS',
            message=messages,
            channelId=channelId,
            sended=True
        )




