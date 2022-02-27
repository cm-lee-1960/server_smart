from datetime import datetime
from django.conf import settings
from django.db.models import Q
from monitor.models import Phone, MeasureCallData, MeasureingTeam, Message

#--------------------------------------------------------------------------------------------------
# 두개의 측정 단말기의 콜 가운트가 동일하고, 메시지 전송기준 콜 수 있지 확인한다.
# 2022.02.25 - 측정 단말기의 총 콜카운트가 아닌 측정 데이터의 현재 콜카운트를 기준으로 메시지 전송여부를 판단한다.
#              단, 측정시작은 현재 콜카운트가 누락될 수 있으니 측정단말의 총 콜카운트가 1일 때로 판단한다.
# 2022.02.27 - 측정시작 메시지 조건 분리 반영
#            - 통신사, 측정유형에 상관없이 측정시작을 판단한다.
#            *** [해결해야할 잠재이슈] 단말 하나로 측정을 하는 경우 주기적인 메시지 전송 판단처리 고민 필요
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
        meastime_from = int(str(mdata.meastime)[:8] + '000000000') # 조회시작
        meastime_to = int(str(mdata.meastime)[:8] + '235959999') # 조회종료
        qs = MeasureCallData.objects.filter(Q(meastime__gte=meastime_from) & Q(meastime__lte=meastime_to))
        if len(qs) <= 1:
            result = True
    elif mdata.currentCount in [3, 10, 27, 37, 57,]:
        # 단말기 체인지 되고 재측정시 그데이터도 더해져서 메시지가 보내질수도 있다 그때는 예외조건
        # 단밀기 그룹으로 묶여 았는 상대편 측정 단말기를 조회한다.
        qs = phone.phoneGroup.phone_set.exclude(phone_no=phone.phone_no)
        if qs.exists():
            p = qs[0]
            # 상대편 측정 단말기의 현재 콜 카운트가 측정 단말 보다 같거나 커야 한다.
            if p.currentCount >= phone.currentCount:
                result = True
        # *** 2022.02.26 측정단말이 하나인 경우 어떻게 처리해야 할지 고민이 필요하다.
        else:
            pass

    return result

#--------------------------------------------------------------------------------------------------
# 측정 단말기의 상태에 따라서 전송 메시지를 생성한다.
#--------------------------------------------------------------------------------------------------
def make_message(mdata):
    """측정단말의 상태에 따라서 메시지를 작성한다."""
    print("make_message()함수 시작")
    # settings.PHONE_STATUS 변수로 선언해도 될지 고민 예정임
    # 2022.01.17 Power On/Off는 데이터 추가해 달라고 하겠음
    # channelId = '-736183270'
    channelId = settings.CHANNEL_ID

    phone = mdata.phone
    status = ["POWERON", "START", "MEASURING", "END"]
    # 측정 진행 메시지는 DL/UP 측정 단말기의 현재 콜 카운트가 같고, 3, 10, 27, 37, 57 콜 단위로 보고함
    if phone.status in status and current_count_check(mdata):
        # 측정 단말기의 DL/UP 평균값들을 가져온다.
        dl_sum, ul_sum, dl_count, ul_count, total_count = 0, 0, 0, 0, 0
        avg_downloadBandwidth = 0  # 다운로드 평균속도
        avg_uploadBandwidth = 0  # 업로드 평균속도
        
   
        # count_check = 0  ## 쌍폰의 카운트 체크
        #
        # # for phone in phone.phoneGroup.phone_set.all():  ## 그룹폰 가져오기
        # for phone_id in phone.phoneGroup.phone_set.all():  ##그룹폰의 목록 카운트
        #     # if 콜카운트가 낮은 phone이면 정보 저장하고 패스
        #     if phone_id.id == phone.id:
        #         # print("이게궁금하다.", phone.id)
        #         dl_count = phone.dl_count  ##현재 dl카운트
        #         avg_downloadBandwidth += phone.avg_downloadBandwidth  ## 현재 dl 에버리지
        #         ul_count = phone.ul_count  ## 현재 ul카운트
        #         avg_uploadBandwidth += phone.avg_uploadBandwidth  ## 현재 ul 에버리지
        #         print(dl_count, avg_downloadBandwidth, ul_count, avg_uploadBandwidth)

        #     else:
        #         for count, measure in enumerate(
        #             Phone.objects.get(id=phone_id.id).measurecalldata_set.all()
        #         ):
        #             if count <= phone.total_count:
        #                 ## 인스턴스여야만한다. 카운트 체크
        #                 g_phone_dl = int(
        #                     0
        #                     if measure.downloadBandwidth == None
        #                     else measure.downloadBandwidth
        #                 )
        #                 g_phone_ul = int(
        #                     0
        #                     if measure.uploadBandwidth == None
        #                     else measure.uploadBandwidth
        #                 )
        #                 ## None값 0으로 초기화

        #                 # dl_count = phone.dl_count  ##현재 카운트
        #                 dl_sum += g_phone_dl
        #                 # ul_count = phone.ul_count  ## 현재 카운트
        #                 ul_sum += g_phone_ul

        #                 print(phone)
        #                 print(
        #                     "####", phone.phone_no, ul_count, dl_count, ul_sum, dl_sum
        #                 )

        #         if dl_sum != 0:
        #             avg_downloadBandwidth += dl_sum / phone.total_count
        #         if ul_sum != 0:
        #             avg_uploadBandwidth += ul_sum / phone.total_count

        # 2022.02.25 현재 메시지를 보내려고 하는 현재 콜카운트와 총 콜카운트를 활용해서 평균값을 산출한다.

        # 2022.02.26 데이터가 맞지 않아 재작성 함       
        # 메시지를 보내려고 하는 측정 단말기
        beforeCount, fpterns = 1, 1
        for m in phone.measurecalldata_set.filter(testNetworkType='speed').order_by("meastime"):
            if total_count > phone.total_count: break
            if m.networkId == 'NR': continue # NR(5G->LTE전환) 데이터 제외
            if m.downloadBandwidth and m.downloadBandwidth > 0:
                dl_sum +=  m.downloadBandwidth
                dl_count += 1
            if m.uploadBandwidth and m.uploadBandwidth > 0:
                    ul_sum += m.uploadBandwidth
                    ul_count += 1
            if m.currentCount < beforeCount: fpterns += 1
            beforeCount = m.currentCount
            total_count += 1
            # print(f"###-1 {phone.phone_no}/{m.currentCount}/{m.downloadBandwidth}/{m.uploadBandwidth }///", mdata.currentCount)
           
        # 상대편 측정 단말기
        qs = phone.phoneGroup.phone_set.filter(ispId='45008', manage=True).exclude(phone_no=phone.phone_no)
        if qs.exists():
            oPhone = qs[0]
            beforeCount, spterns = 1, 1
            for m in oPhone.measurecalldata_set.filter(testNetworkType='speed').order_by("meastime"):
                # 2022.02.25 DL/UL 측정건수가 10건 이상 차이가 나지 않는다는 가정에서 아래 코드가 정상 동작한다.
                if spterns >= fpterns and m. currentCount > m. currentCount: break
                if m.networkId == 'NR': continue # NR(5G->LTE전환) 데이터 제외
                if m.downloadBandwidth and m.downloadBandwidth > 0:
                    dl_sum +=  m.downloadBandwidth
                    dl_count += 1
                if m.uploadBandwidth and m.uploadBandwidth > 0:
                        ul_sum += m.uploadBandwidth
                        ul_count += 1
                if m.currentCount < beforeCount: spterns += 1
                beforeCount = m.currentCount
                # print(f"###-2 {oPhone.phone_no}/{m.currentCount}/{m.downloadBandwidth}/{m.uploadBandwidth }///", mdata.currentCount)

        # DL/UL 평균속도를 산출한다.         
        if dl_count > 0 : avg_downloadBandwidth = round(dl_sum / dl_count,2)
        if ul_count > 0 : avg_uploadBandwidth = round(ul_sum / ul_count,2)

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
        measuringteam_msg = ''
        if phone.status == 'START':
            meastime_str = str(mdata.meastime)
            measdate = datetime.strptime(meastime_str[:8], "%Y%m%d")
            qs = MeasureingTeam.objects.filter(measdate=measdate)
            if qs.exists(): 
                measuringteam_msg = qs[0].message
        START_MSG = f"금일({mmdd}일) S-CXI 품질측정이 {hhmm}분에 {mdata.userInfo1}에서 시작되었습니다.\n" + \
                     f"{measuringteam_msg}\n" + \
                      "\n평가에 만전을 기하여 주시기 바랍니다. "
        # [측정진행 메시지] -----------------------------------------------------------------------------------
        if phone.networkId == 'WiFi':
            MEASURING_MSG = f"{mdata.userInfo1}에서 현재 콜카운트 {mdata.currentCount}번째 측정중입니다.\n" + \
                            "속도(DL/UL, Mbps)\n" + \
                            f"{phone.networkId}(상용): {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}",
        else:
            MEASURING_MSG = f"{mdata.userInfo1}에서 현재 콜카운트 {mdata.currentCount}번째 측정중입니다.\n" + \
                            "(DL/UL/시도호/성공률)\n" + \
                            f"{phone.networkId}: {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}/{phone.total_count}/-"
        # [측정종료 메시지] -----------------------------------------------------------------------------------
        END_MSG = f"금일({mmdd}일) S-CXI 품질측정이 {hhmm}분에 {mdata.userInfo1}을 마지막으로 종료 되었습니다.\n" + \
                   "(DL/UL/시도호/성공률)\n" + \
                            f"{phone.networkId}: {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}/{phone.total_count}/-"
        messages = {
            "POWERON": POWERON_MSG,
            "START": START_MSG,
            "MEASURING": MEASURING_MSG,
            "END": END_MSG,
        }


        # 전송 메시지를 생성한다.
        Message.objects.create(
            phone=phone,
            measdate=str(mdata.meastime)[0:8],
            sendType='TELE',
            userInfo1=mdata.userInfo1,
            currentCount=mdata.currentCount,
            phone_no=mdata.phone_no,
            ownloadBandwidth=avg_downloadBandwidth,
            uploadBandwidth=avg_uploadBandwidth,
            messageType='SMS',
            message=messages[phone.status],
            channelId=channelId,
            sended=True
        )



