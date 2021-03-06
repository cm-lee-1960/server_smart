from datetime import datetime
from django.conf import settings
from django.db.models import Q
from monitor.models import Phone, MeasureCallData, Message
from management.models import MeasureingTeam, ReportCycle, MessageConfig, Center
from monitor.geo import make_map_locations


##################################################################################################################################################
# 측정 시작/진행/종료 메시지를 생성하는 모듈
#
# (F)                       (M)                         (F)                         (C)
# ┌ -----------┐            ┌ -----------┐  post_save   ┌ -----------┐        TELE  ┌ -----------------┐
# |   msg.py   |----------->|  Message   |------------->|  model.py  |----┳-------->|   TelegramBot    |
# └----------- ┘            └----------- ┘   (SIGNAL)   | (monitor)  |    |         |(message.tele_msg)|
# -current_count_check()    -sendType                   └----------- ┘    |         └----------------- ┘
#  .메시지유형 및 작성여부   .TELE: 텔레그램            -send_message()   |         -send_message_bot()
# -make_message()            .XMCS: 크로샷                                |
#  .메시지 작성                                                           |          (F)                            Node.js Module
#                                                                         |          ┌ -----------------┐           ┌ -------------------------┐
#                                                                         └--------->| message.xmcs_msg |---------->| message/sms_broadcast.js |
#                                                                                    └----------------- ┘           └------------------------- ┘
#                                                                                    -send_sms()                    -execute_sms_nodejs.read()
#                                                                                                                               |
#                                                                                                                   ┌ ----------┸--------------┐
#                                                                                                                   |         sms_api.js       |
#                                                                                                                   └------------------------- ┘
#
##################################################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------
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
# 2022.03.15 - 측정시작 메시지 누락 현상 조치 (전송 메시지 내에 메시지 생성 당시의 단말기의 상태정보를 가져감)
# 2022.03.16 - 측정진행 보고 메시지의 주기보고 시점에 대한 복잡도를 낮추기 위해서 단말그룹에 DL/UL 콜카운트 및
#              LTE전환 DL/UL 콜카운트를 가져감
#            - 주기보고 시점은 단말그룸의 콜카운트 정보를 가지고 판단하게 수정함
# 2022.04.08 - 메시지 모델에 단말그룹 추가에 따른 업데이트 코드 추가
# 2022.05.23 - 채널ID를 센터정보에서 가져온다.
# 2022.05.25 - 당일 첫 측정시작인 경우(START_F), 모든 채팅그룹에 메시지를 전송한다.
# 2022.06.08 - DL/UL 속도가 모두 0(Zero)이거나 널(Null)인 경우 측정진행 메시지가 중복 발생하지 않도록 스킵(SKIP)한다.
# ----------------------------------------------------------------------------------------------------------------------
def current_count_check(mdata: MeasureCallData) -> bool:
    """ DL/UL 측정단말의 현재 콜카운트와 보고기준 콜카운트를 확인한다.
        - 파라미터
          . mdata: 측정 데이터(콜단위)
        - 반환값: True or False
    """
    result = False
    phone = mdata.phone
    # 해당지역에 단말이 첫번째로 측정을 시작했는지 확인한다.
    if 'START' in mdata.phone.status:
        # 해당일자에 첫번째 측정 단말기일 경우, 측정시작 메시지를 전송한다.
        # 즉, 해당일자에 측정중인 단말이 없다면 메시지를 전송한다.
        # 측정시작 조건 : 현재 콜카운트가 1인 다른 측정 데이터가 있는지 확인
        # - 결과 <= 1건 : 자기 자신밖에 없으니 측정시작 메시지 전송
        # - 결과 > 1건 : 이미 측정시작 메시지를 전송했으니 메시지를 전송하지 않음
        # 2022.03.11 - 1)전체대상 측정시작 메시지(START_F)
        meastime_from = int(str(mdata.meastime)[:8] + '000000000')  # 조회시작
        meastime_to = int(str(mdata.meastime)[:8] + '235959999')  # 조회종료
        qs = MeasureCallData.objects.filter(Q(meastime__gte=meastime_from) & Q(meastime__lte=meastime_to))
        if mdata.phone.status == 'START_F' and len(qs) <= 1:
            result = True

        # 2022.03.11 - 2)해당지역 측정시작 메시지(START_M)
        # 2-1) 상대편 측정 단말기가 등록되어 있는지 확인한다.
        # 2-2) 상대편 측정 단말기에 속도 측정 데이터가 있는지 확인한다.
        # 2022.03.15 - 측정 데이터가 첫번째 데이터인지 확인하는 사이에 상대편 단말기에 의한 측정 데이터가 생성되어 해당 지역측정 시작 메시지가
        #              누락되는 현상을 막기 위해 명확하게 전송 메시지 내에 단말기 상태를 가져감
        #            - 단말그룹으로 묶여 있는 측정 단말기들로 측정시작 메시지가 전송되었는지를 확인하여 측정시작 메시지를 전송하게 함
        elif mdata.phone.status == 'START_M' and mdata.phone.manage == True:
            phone_list = mdata.phone.phoneGroup.phone_set.all()
            qs = Message.objects.filter(phone__in=phone_list, status='START_M')
            if not qs.exists():
                result = True
    else:
        # 2022.03.16 - 측정진행 보고 메시지의 주기보고 시점에 대한 복잡도를 낮추기 위해서 단말그룹에 DL/UL 콜카운트 및
        #              LTE전환 DL/UL 콜카운트를 가져감
        #            - 주기보고 시점은 단말그룸의 콜카운트 정보를 가지고 판단하게 수정함
        #            - 다운로드 속도나 업로드 속도가 0 이상일 때만 메시지 전송
        #              5G->LTE 전환시 다운로드/업로드 속도가 0인 경우가 있음
        #              예) 경상남도-사천시-남양동 2021.11.01 010-2921-3866 23

        # DL/UL 속도가 모두 0(Zero)이거나 널(Null)인 경우 측정진행 메시지가 중복 발생하지 않도록 스킵(SKIP)한다.
        if (mdata.downloadBandwidth == 0 or mdata.downloadBandwidth is None) and \
                (mdata.uploadBandwidth == 0 or mdata.uploadBandwidth is None):
            return False
        reportCycle = [int(x) for x in ReportCycle.objects.all()[0].reportCycle.split(',')]
        dl_count = phone.phoneGroup.dl_count + phone.phoneGroup.dl_nr_count
        ul_count = phone.phoneGroup.ul_count + phone.phoneGroup.ul_nr_count
        if phone.meastype == 'DL':
            if dl_count in reportCycle and ul_count >= dl_count: result = True
        elif phone.meastype == 'UL':
            if ul_count in reportCycle and dl_count >= ul_count: result = True

        else:
            pass

        # # 모듈검증 코드(삭제예정)
        # print(f"#### {mdata.meastime}/{mdata.phone_no}/{mdata.currentCount}/{phone.meastype}/{dl_count}/{ul_count}/{mdata.downloadBandwidth}/{mdata.uploadBandwidth}/{result}")

    return result


# ----------------------------------------------------------------------------------------------------------------------
# 측정 단말기의 상태에 따라서 전송 메시지를 생성한다.
# 2022.02.27 - 측정 단말기 Power-On/Off 데이터를 별도로 추가 받아야 한다고 함
# 2022.03.05 - 메시지 내용 중에서 숫자에 자동으로 링크가 붙는 것을 조치함 (앞뒤에 <code></code>를 붙임)
# ----------------------------------------------------------------------------------------------------------------------
def make_message(mdata: MeasureCallData):
    """ 측정단말의 상태에 따라서 메시지를 작성한다.
        - 측정단말 상태코드
          . POWERON: 측정단말 파워온(Power-On)
          . START_F: 당일 측정 첫 시작
          . START_M: 해당지역 측정 시작
          . MEASURING: 측정중
          . END: 측정종료
        - 파라미터
          . mdata: 측정 데이터(콜단위)
        - 반환값: 없음
    """

    # 환경변수에서 채팅방 채널IF를 가져온다.
    # channelId = '-736183270'
    # channelId = settings.CHANNEL_ID
    channelId = mdata.phone.center.channelId

    phone = mdata.phone
    status = ["POWERON", "START_F", "START_M", "MEASURING", "END"]
    # 측정 진행 메시지는 DL/UP 측정 단말기의 현재 콜 카운트가 같고, 3, 10, 27, 37, 57 콜 단위로 보고함
    if phone.status in status and current_count_check(mdata):
        # 보고주기 콜카운트를 확인한다.
        reportCallCount = 1
        if phone.meastype == 'DL':
            reportCallCount = phone.phoneGroup.dl_count + phone.phoneGroup.dl_nr_count
        elif phone.meastype == 'UL':
            reportCallCount = phone.phoneGroup.ul_count + phone.phoneGroup.ul_nr_count

        # 측정 단말기의 DL/UP 평균값들을 가져온다.
        # 2022.03.16 - 보고 주기별 속도 평균값이 맞지 않아 다시 작성함
        #              예) 보고주기 3콜이면 DL 3콜, UL 3콜 데이터를 가져와서 평균값을 계산하도록 함
        #              5G->LTE전환은 콜 카운트에는 적용하고 평균값 산출에서는 제외함
        dl_sum, ul_sum, dl_count, ul_count = 0, 0, 0, 0
        dl_nr_count, ul_nr_count = 0, 0  # 5G->LTE 전환콜수(DL, UL)ß
        avg_downloadBandwidth = 0  # 다운로드 평균속도
        avg_uploadBandwidth = 0  # 업로드 평균속도

        total_dl_count, total_ul_count = 0, 0
        phone_list = mdata.phone.phoneGroup.phone_set.all()
        qs = MeasureCallData.objects.filter(phone__in=phone_list, testNetworkType='speed').order_by("meastime")
        msg = mdata.phone.phoneGroup.message_set.all()
        # print("######")
        for m in qs:
            if m.phone.networkId == '5G' and (m.networkId == 'NR' or m.networkId == 'NR5G' or m.nr_check == True):
                # 측정 단말이 5G이고, 측정 데이터가 NR이면 5G->NR 전환 콜수를 하나 증가시킨다.
                if m.downloadBandwidth and m.downloadBandwidth > 0 and total_dl_count < reportCallCount:
                    dl_nr_count += 1
                if m.uploadBandwidth and m.uploadBandwidth > 0 and total_ul_count < reportCallCount:
                    ul_nr_count += 1
            else:
                # 속도 평균값을 구하기 위한 속도 합계와 콜 카운트를 누적한다.
                if m.downloadBandwidth and m.downloadBandwidth > 0 and total_dl_count < reportCallCount:
                    dl_sum += m.downloadBandwidth
                    dl_count += 1
                    # print(f"DL/{m.currentCount}/{m.downloadBandwidth}/-")
                if m.uploadBandwidth and m.uploadBandwidth > 0 and total_ul_count < reportCallCount:
                    ul_sum += m.uploadBandwidth
                    ul_count += 1
                    # print(f"UL/{m.currentCount}/-/{m.uploadBandwidth}")

            # DL/UL 총건수를 계산한다.
            total_dl_count = dl_count + dl_nr_count
            total_ul_count = ul_count + ul_nr_count

            if total_dl_count >= reportCallCount and total_ul_count >= reportCallCount: break

        # 평균속도(DL/UL)를 산출한다.
        if dl_count > 0:
            avg_downloadBandwidth = round(dl_sum / dl_count, 2)  # 평균속도(DL)
        if ul_count > 0:
            avg_uploadBandwidth = round(ul_sum / ul_count, 2)  # 평균속도(UL)

        # print(f"##### {avg_downloadBandwidth}/{dl_count}/{avg_uploadBandwidth}/{ul_count}")

        # 메시지를 작성한다.
        #                01234567890123456
        # last_updated : 20211101235959999
        last_updated_str = str(mdata.phone.last_updated)
        mmdd = last_updated_str[4:6] + "." + str(int(last_updated_str[6:8]))
        hhmm = last_updated_str[8:10] + ":" + last_updated_str[10:12]
        # [파워온 메시지] ----------------------------------------------------------------------------------------------
        POWERON_MSG = f"{mdata.userInfo1}에서 단말이 켜졌습니다."
        # [측정시작 메시지] --------------------------------------------------------------------------------------------
        # 당일 측정조 메시지 내용을 가져온다.

        sendType = 'TELE'
        if phone.status == 'START_F' and mdata.ispId == '45008':
            sendType = 'ALL' # 전송유형(문자 메시지와 텔레그램에 동시에 전송)
            measuringteam_msg = ''  # 당일 측정조 (데이터베이스에서 가져와야 함)
            meastime_str = str(mdata.meastime)
            measdate = datetime.strptime(meastime_str[:8], "%Y%m%d")
            qs = MeasureingTeam.objects.filter(measdate=measdate)
            if qs.exists():
                measuringteam_msg = qs[0].message
            messages = f"금일({mmdd}일) S-CXI 품질측정이 {hhmm}분에 {mdata.userInfo1}에서 시작되었습니다.({mdata.networkId})\n" + \
                       f"{measuringteam_msg}\n" + \
                       "\n평가에 만전을 기하여 주시기 바랍니다. "
        elif phone.status == 'START_M':
            if mdata.phone.networkId == 'WiFi':
                messages = f"S-CXI {mdata.phone.morphology}({mdata.phone.phoneGroup.morphologyDetail}) {mdata.userInfo1} 측정시작({mdata.time}~)"
            else:
                if phone.measuringTeam is not None:
                    messages = f"S-CXI {phone.measuringTeam} {mdata.phone.morphology}({mdata.phone.networkId}) {mdata.userInfo1} 측정시작({mdata.time}~)"
                else:
                    messages = f"S-CXI {mdata.phone.morphology}({mdata.phone.networkId}) {mdata.userInfo1} 측정시작({mdata.time}~)"

        # [측정진행 메시지] --------------------------------------------------------------------------------------------
        elif phone.status == 'MEASURING':
            # WiFi 측정 데이터의 경우
            if phone.networkId == 'WiFi':
                messages = f"S-CXI {phone.measuringTeam} {phone.networkId} {mdata.userInfo1} 현재 콜카운트 {reportCallCount}번째 측정중입니다.\n" + \
                           "- 속도(DL/UL, Mbps)\n" + \
                           f" {phone.networkId}({phone.phoneGroup.morphologyDetail.main_class}): {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}"
            # 5G 측정 데이터의 경우
            elif phone.networkId == '5G':
                messages = f"S-CXI {phone.measuringTeam} "
                if phone.phoneGroup.morphologyDetail is not None:
                    messages += f"{phone.phoneGroup.morphologyDetail.network_type} "
                else: messages += f"{phone.networkId} "
                messages += f"{mdata.userInfo1} 측정\n({phone.starttime}~, {reportCallCount}콜 진행중)\n" + \
                           f"- 속도(DL/UL, Mbps): {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}\n" + \
                           f"- LTE 전환(DL/UL, 콜): {dl_nr_count}/{ul_nr_count}"
            # 기타(LTE, 3G) 측정데이터의 경우
            else:
                messages = f"S-CXI {phone.measuringTeam} {phone.networkId} {mdata.userInfo1} 측정\n({phone.starttime}~, {reportCallCount}콜 진행중)\n" + \
                           f"- 속도(DL/UL, Mbps): {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}"
            # 이벤트 메시지 내용 추가
            messages +=  f"\n- 속도저하 이벤트(DL/UL, 건): {msg.filter(message__contains='DL속도저하', center=phone.center).count()}/{msg.filter(message__contains='UL속도저하', center=phone.center).count()}" + \
                         f"\n- 전송실패 이벤트(DL/UL, 건): {msg.filter(message__contains='DL전송실패', center=phone.center).count()}/{msg.filter(message__contains='UL전송실패', center=phone.center).count()}"


        # [측정종료 메시지] --------------------------------------------------------------------------------------------
        # 2022-03-11 - 측정종료 메시지는 수기로 해당지역 측정종료 및 당일 측정종료를 실행할 때 생성되기 때문에 여기에 있는 코드를 사용하지 않음
        elif phone.status == 'END':
            messages = f"금일({mmdd}일) S-CXI 품질측정이 {hhmm}분에 {mdata.userInfo1}을 마지막으로 종료 되었습니다.\n" + \
                       "(DL/UL/시도호/성공률)\n" + \
                       f"{phone.networkId}: {avg_downloadBandwidth:.1f}/{avg_uploadBandwidth:.1f}/{dl_count + ul_count}/-</>"

        # 2022.03.17 - 보안이슈로 지도맵 기능제공 취소함
        # # 해당 측정위치에 대한 지도맵을 작성하고, 메시지 하단에 [지도보기] 링크를 붙인다.
        # filename = make_map_locations(mdata)
        # messages += f"\n<a href='http://127.0.0.1:8000/monitor/maps/{filename}'>지도보기</a>"

        # 전송 메시지를 생성한다.
        message = Message.objects.create(
            phoneGroup=phone.phoneGroup, # 단말그룹
            phone=phone,  # 측정단말
            center=phone.phoneGroup.center,
            status=phone.status,
            # 측정단말 상태코드(POWERON:파워온,START_F:측정첫시작,START_M:측정시작,MEASURING:측정중,END:측정종료,END_LAST:마지막지역측정종료,REPORT:일일보고용,REPORT_ALL:일일보고용전체)
            measdate=str(mdata.meastime)[0:8],  # 측정일자
            sendType=sendType,  # 전송유형(TELE: 텔레그램, XMCS: 크로샷)
            userInfo1=mdata.userInfo1,  # 측정자 입력값1
            currentCount=mdata.currentCount,  # 현재 콜카운트
            phone_no=mdata.phone_no,  # 측정단말 전화번호
            downloadBandwidth=avg_downloadBandwidth,  # DL 평균속도
            uploadBandwidth=avg_uploadBandwidth,  # UL 평균속도
            messageType='SMS',  # 메시지 유형(SMS: 측정 메시지, EVENT: 이벤트발생 메시지)
            message=messages,  # 메시지 내용
            channelId=channelId,  # 채널ID
        )

        # 당일 첫 측정시작인 경우(START_F), 모든 채팅그룹에 메시지를 전송한다.
        channelId_list = [channelId,]
        if phone.status == 'START_F':
            qs = Center.objects.all()
            if qs.exists():
                for center in qs:
                    if center.channelId not in channelId_list:
                        message.pk = None
                        message.center = center
                        message.channelId = center.channelId
                        message.save()
                        channelId_list.append(center.channelId)


def event_type_check(message):
    """메시지의 이벤트 유형 체크 함수
        .파라미터 : 메시지 쿼리셋
        .반환값 : 리스트"""
    eventTypes = []
    if '전송실패' in message.message:
        eventTypes.append('eventFailure')
    if '속도저하' in message.message:
        eventTypes.append('eventLowThroughput')
    if '음성 콜 드랍' in message.message:  # 음성 콜 드랍 메시지 확정 시 수정
        eventTypes.append('eventVoiceDrop')
    if 'LTE전환' in message.message:
        eventTypes.append('eventNR')
    if '측정범위 벗어남' in message.message:
        eventTypes.append('evntOffZone')
    if '측정단말 한곳에 머뭄' in message.message:
        eventTypes.append('eventStay')
    if '중복측정' in message.message:
        eventTypes.append('eventDuplication')
    return eventTypes

def check_message_send(message):
    """메시지 전송여부 함수
        .파라미터 : 메시지 쿼리셋
        .반환값 : Boolean(True or False)"""
    if message.sendType == "XMCS":
        return False

    elif MessageConfig.objects.get(messageStatus='ALL').booleanValue == False:
        return False
    elif message.phoneGroup and message.phoneGroup.autoSend == False:
        return False
    elif message.messageType == 'EVENT':
        eventTypes = event_type_check(message)
        eventStatus = MessageConfig.objects.filter(booleanValue=True).values_list('messageStatus', flat=True)
        sendStatus = []
        for event in eventTypes:
            if event in eventStatus:
                return True
            else: pass
        return False

    elif MessageConfig.objects.filter(messageStatus=message.status).exists():
        return MessageConfig.objects.get(messageStatus=message.status).booleanValue
    else:
        return True