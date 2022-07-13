from management.models import PhoneInfo, Center
from .models import PhoneLoc, Message

########################################################################################################################
# 수신데이터를 처리하는 모듈
# 1) 측정단말 위치정보 데이터 저장
# 2) 측정단말 사전정보 업데이트
# 3) 텔레그램 메시지 생성(파워온: POWER_ON)
# ----------------------------------------------------------------------------------------------------------------------
# 2022.06.28 - 측정단말 위치정보 수신데이터 처리 모듈 작성
# 2022.07.12 - 이벤트타입(eventType)에 따라 처리로직 반영
#
########################################################################################################################

def phoneloc_proc(data):
    # 수신 받은 JSON 데이터를 파싱한다.
    # [ 항목 ]
    #  - dataType: loc # 문자 형식
    #  - phone_no: 1012341234 # 숫자
    #  - cellId : 12345678 #문자 형식
    #  - eventType : # 문자 형식
    #  - addressDetail : 서울특별시 은평구 녹번동 105-50 # 문자
    #  - last_updated:  20220620123056000    #전송시간 # 숫자
    result = None

    # ------------------------------------------------------------------------------------------------------------------
    # 1) 측정단말 위치정보를 저장한다.
    # ------------------------------------------------------------------------------------------------------------------
    phoneLoc = PhoneLoc.objects.create(**data)

    # 2),3) 항목은 측정단말 서전정보에 등록된 건에 대해서만 처리하도록 한다.
    # 해당 측정단말 번호로 사전 등록된 정보가 있는지 조회한다.
    qs = PhoneInfo.objects.filter(phone_no=data['phone_no'])
    if qs.exists():
        # --------------------------------------------------------------------------------------------------------------
        # 2) 측정단말 사전정보의 위치정보, 파워 온/오프 항목을 업데이트 한다.
        # --------------------------------------------------------------------------------------------------------------
        phoneInfo = qs[0]
        eventType = data['eventType']   # 이벤트타입
        phoneInfo.addressDetail = data['addressDetail']     # 최종위치
        if eventType == "AttachRequest":
            phoneInfo.power = True
        elif eventType == "DetachRequest":
            phoneInfo.power = False
        else:
            phoneInfo.power = True

        # 측정단말 사전정보를 업데이트 한다.
        phoneInfo.save()

        # --------------------------------------------------------------------------------------------------------------
        # 3) 텔레그램 메시지를 생성한다.
        # --------------------------------------------------------------------------------------------------------------
        if eventType == "AttachRequest":
            measdate = str(phoneLoc.last_updated)[:8] # 측정일자
            status = 'POWER_ON'
            msg_qs = Message.objects.filter(measdate=measdate, phone_no=phoneLoc.phone_no, status=status)
            if not msg_qs.exists():
                # S-CXI 2조 (networkId) (주소) 단말 power on (시간)
                message_text = f"S-CXI {phoneInfo.measuringTeam} ({phoneInfo.networkId}) ({phoneLoc.addressDetail}) 단말 Power On ({phoneInfo.last_updated_time})"
                # 운용본부 텔레그램 채널ID를 조회한다.
                channelId = None
                cnt_qs = Center.objects.filter(centerName='운용본부')
                if cnt_qs.exists():
                    channelId = cnt_qs[0].channelId
                # 해당 측정단말에 대한 파워온 메시지를 생성한다.
                message = Message.objects.create(
                    phoneGroup=None,    # 단말그룹
                    phone=None,         # 측정단말
                    center=None,        # 관할센터
                    status='POWER_ON',  #  POSER_ON: 마지막 종료 시의 메시지
                    measdate=measdate,  # 측정일자
                    sendType='TELE',    # 전송유형(TELE: 텔레그램, XMCS: 크로샷, ALL: 모두)
                    userInfo1=phoneLoc.addressDetail,  # 상세주소
                    phone_no=phoneLoc.phone_no,  # 측정단말 전화번호
                    downloadBandwidth=None, # DL속도
                    uploadBandwidth=None,   # UL속도
                    messageType='SMS',      # 메시지유형(SMS: 메시지, EVENT: 이벤트)
                    message=message_text,   # 메시지 내용
                    channelId=channelId,    # 채널ID
                    sended=False  # 전송여부 : Message 모델의 sendType이 ALL일 경우 수동으로 크로샷까지 보내야 True로 변경(텔레그램만 전송한 경우 False 유지)
                )

        result = "처리완료"

    return result