from email import message
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Max, Min, Avg, Count, Q
from django.db import connection

from .models import Phone, PhoneGroup, MeasureCallData, MeasureSecondData, Message, MeasuringDayClose, TestDayClose
from management.models import Center, Morphology

from .serializers import PhoneGroupSerializer
from message.tele_msg import TelegramBot
from datetime import datetime

########################################################################################################################
# 측정종료 및 측정마감 모듈
# 1) 측정종료 - 해당지역에 대한 측정을 종료처리
# 2) 측정마감 - 당일 모든 측정을 종료처리
#                                                                                           (M)메시지
# ┌ -----------┐            ┌ -----------┐             ┌ -----------┐   측정종료/측정마감  ┌ -----------┐
# |   url.py   |----------->|  views.py  |------------>|  close.py  |----------┳---------->|  Message   |
# └----------- ┘            └----------- ┘             └----------- ┘          |           └----------- ┘
# - monitor/end             - measuring_end_view        - measuring_end        |          (M)측정마감
# - monitor/close           - measuring_day_close_view  - measuring_day_close  |측정마감  ┌-------------------┐
#                                                                              └--------->| MeasuringDayClose |
#                                                                                         └------------------ ┘
# [ 메시지 작성 흐름도 ]
#                            status='END'
# ┌ ------------┐            ┌ ------------------------------------------------------------------------------------┐
# |  측정종료   |----┯------>| ㅇS-CXI 1조 5G 서울특별시-수도권 5호선(방화-하남검단산) 측정종료(07:40~10:20, 95콜) |
# └-----∧------ ┘    |       |   - LTE 전환율(DL/UL, %): 0 / 14                                                    |
#       |            |       |   - 속도(DL/UL, Mbps): 1003.8 / 82.5                                                |
#       |            |       └------------------------------------------------------------------------------------ ┘
#       |            |       status='END_LAST'
#       |            |       ┌ ------------------------------------------------------------------------------------┐
#       |            |       | ㅇ                                                                                  |
#       |            ┗------>|   -                                                                                 |
#       |                    |   -                                                                                 |
#       |(측정미종료시/      └------------------------------------------------------------------------------------ ┘
#       | active=True)
#       |                    status='REPORT'
# ┌ ----┻-------┐            ┌ --------------------------------------------------┐
# |  측정마감   |----┯------>| ㅇ 서울특별시-수도권 5호선(방화-하남검단산)(테마) |
# └------------ ┘    |       |   - (DL/UL/시도호/전송성공률)                     |
#                    |       |    .5G "1003.6/82.3/105/100.0"                    |
#                    |       |   ※ LTE전환율(DL/UL),접속/지연시간                |
#                    |       |    .0.0/12.0%,접속시간계산(업데이트예정)/16.3ms'  |
#                    |       └-------------------------------------------------- ┘
#                    |       status='REPORT_ALL'
#                    |       ┌ -----------------------------------------------------┐
#                    |       | 금일 품질 측정 결과를 아래와 같이 보고 드립니다.     |
#                    |       | ㅇ 서울특별시-수도권 5호선(방화-하남검단산)(테마)    |
#                    |       |   - (DL/UL/시도호/전송성공률)                        |
#                    ┗------>|    .5G "1003.6/82.3/105/100.0"                       |
#                            |   ※ LTE전환율(DL/UL),접속/지연시간                   |
#                            |    .0.0/12.0%,접속시간계산(업데이트예정)/16.3ms      |
#                            |                                                      |
#                            | ㅇ 경상남도-통영시-정량동(행정동)                    |
#                            |  - (DL/UL/시도호/전송성공률)                         |
#                            |    .5G "684.2/89.3/53/100                            |
#                            |  ※ LTE전환율(DL/UL),접속/지연시간                    |
#                            |   .0.0/1.9%,접속시간계산(업데이트예정)/28.5ms        |
#                            |                                                      |
#                            |  (생략)                                              |
#                            └----------------------------------------------------- ┘
#
# ----------------------------------------------------------------------------------------------------------------------
# 2022-03-21 - 확정된 모듈과 입시 모듈의 순서 변경 및 주석 추가
# 2022-03-25 - 측정종료 및 측정마감 흐름도 작성 및 주석 추가
# 2022-03.30 - 측정종료 및 측정마감 메시지 작성 흐름도 및 주석 추가
#
########################################################################################################################

########################################################################################################################
# 해당지역의 측정을 종료한다.
# 1) 해당지역 측정종료 메시지 생성
# 2) 해당지역 측정종료 데이터 저장
# 3) 당일 측정종료 메시지 생성(하루 한번)
########################################################################################################################
def measuring_end(phoneGroup):
    """ 해당지역의 측정을 종료하는 함수
      - 파라미터
        . phoneGroup: 단말그룹(PhoneGroup)
      - 반환값: dict {result : 결과값} // 성공 시 결과값 'ok'
    """
    if phoneGroup.active == False:  # 이미 종료한 지역일 경우 pass 처리
        return_value = {'result' : 'ERROR: 이미 측정 종료한 지역'}
        return return_value
    else:
        # 해당 단말그룹에 묶여 있는 단말기들을 가져온다.
        try:
            # --------------------------------------------------------------------------------------------------------------
            # 1) 측정종료된 단말그룹에 대한 측정종료 메시지를 생성한다.
            # --------------------------------------------------------------------------------------------------------------
            phone_list = phoneGroup.phone_set.all()
            # 총 콜카운트를 가져온다.
            avg_bandwidth = cal_avg_bw_call(phoneGroup)  # 평균속도 계산
            nr_percent = cal_nr_percent(phoneGroup)  # 5G -> LTE 전환율 계산
            total_count = max(phoneGroup.dl_count + phoneGroup.dl_nr_count, phoneGroup.ul_count + phoneGroup.ul_nr_count)
            # 측정시작 시간과 측정종료 시간을 확인한다.
            qs = MeasureCallData.objects.filter(phone__in=phone_list, testNetworkType='speed').order_by("meastime")
            meastime_max_min = qs.aggregate(Max('meastime'), Min('meastime'))
            globals().update(meastime_max_min)
            start_meastime = str(meastime__min)[8:10] + ':' + str(meastime__min)[10:12]
            end_meastime = str(meastime__max)[8:10] + ':' + str(meastime__max)[10:12]

            # 메시지를 작성한다.
            message = f"ㅇS-CXI {phoneGroup.measuringTeam} {phoneGroup.networkId} {phoneGroup.userInfo1} " + \
                    f"측정종료({start_meastime}~{end_meastime}, {total_count}콜)\n"
            # 5G의 경우 메시지 내용에 LTE전환율 포함한다.
            if phoneGroup.networkId == '5G':
                message += f"- LTE 전환율(DL/UL, %): {nr_percent['dl_nr_percent']} / {nr_percent['ul_nr_percent']}\n"
            # 평균 속도값을 메시지에 추가한다.
            message += f"- 속도(DL/UL, Mbps): {avg_bandwidth['avg_downloadBandwidth']} / {avg_bandwidth['avg_uploadBandwidth']}"
            # 메시지를 저장한다.
            try: # phonegroup과 foreign-key 로 묶인 center 의 channelId 를 가져온다.
                chatId = phoneGroup.center.channelId
            except Exception as e: # 묶인 center가 없으면 channelId는 None
                chatId = None
                print("메시지의 channelId가 없습니다. 센터 정보를 확인해주세요.: ", str(e))
                raise Exception("measuring_end() - no channelId: %s" % e)
            
            message_end = Message.objects.filter(measdate=phoneGroup.measdate, userInfo1=phoneGroup.userInfo1, status='END')
            if message_end.exists():
                message_end.delete()  # 메시지는 생성될 때에만 전송되기때문에 이전 메시지는 삭제
                message_end = Message.objects.create(
                    phoneGroup=phoneGroup,
                    phone=None, # 측정단말
                    status='END', # 진행상태(POWERON:파워온, START_F:측정첫시작, START_M:측정시작, MEASURING:측정중, END:측정정료)
                    measdate=phoneGroup.measdate, # 측정일자
                    sendType='ALL', # 전송유형(TELE: 텔레그램, XMCS: 크로샷, ALL: 모두)
                    userInfo1=phoneGroup.userInfo1, # 측정자 입력값1
                    phone_no=None, # 측정단말 전화번호
                    downloadBandwidth=avg_bandwidth['avg_downloadBandwidth'], # DL속도
                    uploadBandwidth=avg_bandwidth['avg_uploadBandwidth'], # UL속도
                    messageType='SMS', # 메시지유형(SMS: 메시지, EVENT: 이벤트)
                    message=message, # 메시지 내용
                    channelId=chatId, # 채널ID
                    sended=False # 전송여부 : Message 모델의 sendType이 ALL일 경우 수동으로 크로샷까지 보내야 True로 변경(텔레그램만 전송한 경우 False 유지)
                )
            else:
                message_end = Message.objects.create(
                    phoneGroup=phoneGroup,
                    phone=None, # 측정단말
                    status='END', # 진행상태(POWERON:파워온, START_F:측정첫시작, START_M:측정시작, MEASURING:측정중, END:측정정료)
                    measdate=phoneGroup.measdate, # 측정일자
                    sendType='ALL', # 전송유형(TELE: 텔레그램, XMCS: 크로샷, ALL: 모두)
                    userInfo1=phoneGroup.userInfo1, # 측정자 입력값1
                    phone_no=None, # 측정단말 전화번호
                    downloadBandwidth=avg_bandwidth['avg_downloadBandwidth'], # DL속도
                    uploadBandwidth=avg_bandwidth['avg_uploadBandwidth'], # UL속도
                    messageType='SMS', # 메시지유형(SMS: 메시지, EVENT: 이벤트)
                    message=message, # 메시지 내용
                    channelId=chatId, # 채널ID
                    sended=False # 전송여부 : Message 모델의 sendType이 ALL일 경우 수동으로 크로샷까지 보내야 True로 변경(텔레그램만 전송한 경우 False 유지)
                )
            
            # 측정종료 처리가 완료된 단말그룹과 측정단말의 상태를 비활성화 시킨다.
            phoneGroup.active = False # 단말그룹
            phoneGroup.save()
            phone_list.update(active=False) # 측정단말

            # --------------------------------------------------------------------------------------------------------------
            # 2) 측정종료된 단말그룹에 대한 마감데이터를 생성한다.
            #   - 신규 데이터: 생성(Create)
            #   - 기존 데이터: 업데이트(Update)
            # --------------------------------------------------------------------------------------------------------------
            # 해당 단말그룹에 대한 측정종료 데이터가 있는지 확인한다.
            md = MeasuringDayClose.objects.filter(measdate=phoneGroup.measdate, phoneGroup=phoneGroup)
            # 직렬화 대상 필드를 지정한다.
            fields = ['center_id', 'morphology_id', 'measdate', 'userInfo1', 'networkId', \
                    'dl_count', 'ul_count', 'dl_nr_count', 'ul_nr_count']
            serializer = PhoneGroupSerializer(phoneGroup, fields=fields)
            if md.exists(): # 기존에 생성된 데이터가 있으면
                # 해당 단말그룹에 대한 측정종료 데이터를 업데이트 한다
                md.update(**serializer.data)
                # 평균속도, 전환율, 총 콜 수는 새로이 계산한 값으로 저장한다.
                md.update(downloadBandwidth=avg_bandwidth['avg_downloadBandwidth'], \
                        uploadBandwidth=avg_bandwidth['avg_uploadBandwidth'], \
                        dl_nr_percent=nr_percent['dl_nr_percent'], ul_nr_percent=nr_percent['ul_nr_percent'], \
                        total_count=total_count)
            else: # 기존에 생성된 데이터가 없으면
                # 해당 단말그룹에 대한 측정종료 데이터를 데이터베이스에 저장한다.
                MeasuringDayClose.objects.create(phoneGroup=phoneGroup, \
                                                downloadBandwidth=avg_bandwidth['avg_downloadBandwidth'],
                                                uploadBandwidth=avg_bandwidth['avg_uploadBandwidth'], \
                                                dl_nr_percent=nr_percent['dl_nr_percent'], ul_nr_percent=nr_percent['ul_nr_percent'], \
                                                total_count=total_count, \
                                                **serializer.data)
            # 측정마감 테스트################################################################
            hj = TestDayClose.objects.filter(measdate=phoneGroup.measdate, phoneGroup=phoneGroup)
            a = Phone.objects.filter(phoneGroup_id = phoneGroup.id, userInfo1 = phoneGroup.userInfo1, userInfo2 = phoneGroup.userInfo2, measdate = phoneGroup.measdate)
            siDo = a[0].siDo
            guGun = a[0].guGun
            addressDetail = a[0].addressDetail
            if a[0].morphology_id == 1:
                mopo = "행정동"
                if "특별시" in a[0].siDo or "광역시" in a[0].siDo:
                        address = "대도시"
                elif a[0].guGun.endswith("읍") or  a[0].guGun.endswith("면"):
                        address = "농어촌"
                else:
                        address = "중소도시"
            elif a[0].morphology_id == 2:
                mopo = "테마"
                if "병원" in a[0].userInfo1:
                    mopo = "인빌딩"
                    address = "대형병원"
                elif "백화점" in a[0].userInfo1:
                    mopo = "인빌딩"
                    address = "백화점"
                elif "터미널" in a[0].userInfo1:
                    mopo = "인빌딩"
                    address = "터미널"
                elif "역" in a[0].userInfo1:
                    mopo = "인빌딩"
                    address = "역사"
                elif "공항" in a[0].userInfo1:
                    mopo = "인빌딩"
                    address = "공항" 
                elif "대학" in a[0].userInfo1 or "학생" in a[0].userInfo1:
                    mopo = "테마"
                    address = "대학교"
                elif "공원" in a[0].userInfo1:
                    mopo = "테마"
                    address = "놀이공원"
                elif "거리" in a[0].userInfo1:
                    mopo = "테마"
                    address = "주요거리" 
                else:
                    address = "수정필요"           
            elif a[0].morphology_id == 3:
                mopo = "인빌딩"
            elif a[0].morphology_id== 4:
                mopo = "커버리지"
            elif a[0].morphology_id== 5 or a[0].userInfo2 == "L" or a[0].userInfo2 == "3":
                mopo = "취약지역"
                if a[0].userInfo1.endswith("도"):
                    address = "유인도서"
                elif a[0].userInfo1.endswith("산"):
                    address = "등산로"
                elif "해안도로" in a[0].userInfo1:
                    address = "해안도로"
                elif "-" in a[0].userInfo1:
                    address = "여객항로"
                else: 
                    address = "수정필요"
            else:
                pass
            if a[0].networkId == "WiFi":
                if "개" in a[0].userInfo2: 
                    address = "개방"
                elif "상" in a[0].userInfo2:
                    address = "상용"
                else:
                    address = "수정필요" 
            else:
                pass
            if "서울" in a[0].siDo or "서울" in a[0].guGun:
                district = "서울"
            elif "인천" in a[0].siDo or "인천" in a[0].guGun:
                district = "인천"
            elif "울산" in a[0].siDo or "울산" in a[0].guGun:
                district = "울산"
            elif "대구" in a[0].siDo or "대구" in a[0].guGun:
                district = "대구"
            elif "광주" in a[0].siDo or "광주" in a[0].guGun:
                district = "광주"
            elif "대전" in a[0].siDo or "대전" in a[0].guGun:
                district = "대전"
            elif "경기" in a[0].siDo or "경기" in a[0].guGun:
                district = "경기"
            elif "경상북" in a[0].siDo or "경상북" in a[0].guGun:
                district = "경북"
            elif "경상남" in a[0].siDo or "경상남" in a[0].guGun:
                district = "경남"
            elif "전라남" in a[0].siDo or "전라남" in a[0].guGun:
                district = "전남"
            elif "전라북" in a[0].siDo or "전라북" in a[0].guGun:
                district = "전북"
            elif "충청남" in a[0].siDo or "충청남" in a[0].guGun:
                district = "충남"
            elif "충청북" in a[0].siDo or "충청북" in a[0].guGun:
                district = "충북"
            elif "세종" in a[0].siDo or "세종" in a[0].guGun:
                district = "세종"
            else:
                district = "수도권"
            lte_percent = ((a[0].nr_count)/a[0].total_count)*100
             # 직렬화 대상 필드를 지정한다.
            # fields = ['center_id', 'morphology_id', 'measdate', 'userInfo1', 'userInfo2', 'networkId', \
            #         'dl_count', 'ul_count', 'dl_nr_count', 'ul_nr_count']
            fields = ['center_id','measdate', 'userInfo1', 'networkId']
            serializer = PhoneGroupSerializer(phoneGroup, fields=fields)
            if hj.exists():
                # 해당 단말그룹에 대한 측정종료 데이터를 데이터베이스에 저장한다.
                hj.update(**serializer.data)
                
                
                # 평균속도, 전환율, 총 콜 수는 새로이 계산한 값으로 저장한다.
                
                hj.update(downloadBandwidth=avg_bandwidth['avg_downloadBandwidth'], \
                        uploadBandwidth=avg_bandwidth['avg_uploadBandwidth'], \
                        # siDo = siDo, guGun = guGun, addressDetail = addressDetail,\
                        # dl_nr_percent=nr_percent['dl_nr_percent'], ul_nr_percent=nr_percent['ul_nr_percent'], \
                        address=address, mopo=mopo,district=district,lte_percent=lte_percent)
                        # total_count=total_count)
            else:
                
                # 해당 단말그룹에 대한 측정종료 데이터를 업데이트 한다
                TestDayClose.objects.create(phoneGroup=phoneGroup, \
                                                # siDo =siDo, guGun = guGun, addressDetail =addressDetail, \
                                                downloadBandwidth=avg_bandwidth['avg_downloadBandwidth'], \
                                                uploadBandwidth=avg_bandwidth['avg_uploadBandwidth'], \
                                                # dl_nr_percent=nr_percent['dl_nr_percent'], ul_nr_percent=nr_percent['ul_nr_percent'], \
                                                address=address, mopo=mopo,district=district,lte_percent=lte_percent, \
                                                # total_count=total_count, \
                                                **serializer.data)
                                                
        ###########################################################################################################################   
        except Exception as e:
            print("측정종료 메시지 및 데이터 저장: ", str(e))
            raise Exception("measuring_end() - 측정종료 메시지 및 데이터 저장: %s" % e)
        

        # ------------------------------------------------------------------------------------------------------------------
        # 3) 해당 단말그룹이 당일 측정종료 최종 마지막일 때 당일 측정종료 메시지를 생성한다.
        # ------------------------------------------------------------------------------------------------------------------
        try:
            # 더 이상 활성화된 단말그룹이 없다면 최종 마지막 단말그룹이라고 판단한다.
            # 즉, 가장 마지막 측정종료 단말그룹이라는 것을 의미한다.
            if PhoneGroup.objects.filter(measdate=phoneGroup.measdate, ispId=45008, manage=True, active=True).count() == 0:
                # 측정지역 개수 추출
                daily_day = str(phoneGroup.measdate)[4:6] + '월' + str(phoneGroup.measdate)[6:8] + '일'
                # 네트워크 유형별 건수를 조회한다.
                cursor = connection.cursor()
                cursor.execute(" SELECT networkId, COUNT(*) AS COUNT " + \
                                "      FROM monitor_phonegroup " + \
                                f"      WHERE measdate='{phoneGroup.measdate}' and " + \
                                "             ispId = '45008' and " + \
                                "             manage = True " + \
                                "      GROUP BY networkId "
                                )
                result = dict((x, y) for x, y in [row for row in cursor.fetchall()])
                fiveg_count = result['5G'] if '5G' in result.keys() else 0 # 5G 측정건수
                lte_count = result['LTE'] if 'LTE' in result.keys() else 0 # LTE 측정건수
                threeg_count = result['3G'] if '3G' in result.keys() else 0 # 3G 측정건수
                wifi_count = result['WiFi'] if 'WiFi' in result.keys() else 0 # WiFi 측정건수
                total_count = fiveg_count + lte_count + threeg_count + wifi_count
                # 네트워크 유형 별 userInfo1을 추출한다.
                userInfo_byType = {'5G':'', 'LTE':'', '3G':'', 'WiFi':''}
                for userInfo in PhoneGroup.objects.filter(measdate=phoneGroup.measdate, ispId=45008).values('networkId', 'userInfo1'):
                    userInfo_byType[userInfo['networkId']] += '\n  .' + userInfo['userInfo1']

                # 메시지를 생성한다.
                message_end_last = f"금일({daily_day}) S-CXI 품질 측정이 {end_meastime}분에 " + \
                            f"{phoneGroup.userInfo1}({phoneGroup.networkId}{phoneGroup.morphology})을 마지막으로 종료 되었습니다.\n" + \
                            f"ㅇ 측정지역({total_count})\n" + \
                            f" - 5G품질({fiveg_count})\n" + f"  .{userInfo_byType['5G']}\n" + \
                            f" - LTE/3G 취약지역 품질({lte_count + threeg_count})\n" + f"  .{userInfo_byType['LTE']}\n" + f"  .{userInfo_byType['LTE']}\n" + \
                            f" - WiFi 품질({wifi_count})\n" + f"  .{userInfo_byType['WiFi']}\n" + \
                            "수고 많으셨습니다."

                # 마지막 종료 메시지가 존재하면 update, 미존재면 신규생성
                message_last_exists = Message.objects.filter(measdate=phoneGroup.measdate, status='END_LAST')
                if message_last_exists.exists():
                    message_last_exists.delete()  # 메시지는 생성될 때에만 전송되기때문에 이전 메시지는 삭제
                    message_last_exists = Message.objects.create(
                        phoneGroup=phoneGroup,
                        phone=None, # 측정단말
                        status='END_LAST',  # END_LAST : 마지막 종료 시의 메시지
                        measdate=phoneGroup.measdate, # 측정일자
                        sendType='ALL', # 전송유형(TELE: 텔레그램, XMCS: 크로샷, ALL: 모두)
                        userInfo1=phoneGroup.userInfo1, # 측정자 입력값1
                        phone_no=None, # 측정단말 전화번호
                        downloadBandwidth=None, # DL속도
                        uploadBandwidth=None, # UL속도
                        messageType='SMS', # 메시지유형(SMS: 메시지, EVENT: 이벤트)
                        message=message_end_last, # 메시지 내용
                        channelId=chatId, # 채널ID
                        sended=False # 전송여부 : Message 모델의 sendType이 ALL일 경우 수동으로 크로샷까지 보내야 True로 변경(텔레그램만 전송한 경우 False 유지)
                        )
                else:
                    message_last_exists = Message.objects.create(
                        phoneGroup=phoneGroup,
                        phone=None, # 측정단말
                        status='END_LAST',  # END_LAST : 마지막 종료 시의 메시지
                        measdate=phoneGroup.measdate, # 측정일자
                        sendType='ALL', # 전송유형(TELE: 텔레그램, XMCS: 크로샷, ALL: 모두)
                        userInfo1=phoneGroup.userInfo1, # 측정자 입력값1
                        phone_no=None, # 측정단말 전화번호
                        downloadBandwidth=None, # DL속도
                        uploadBandwidth=None, # UL속도
                        messageType='SMS', # 메시지유형(SMS: 메시지, EVENT: 이벤트)
                        message=message_end_last, # 메시지 내용
                        channelId=chatId, # 채널ID
                        sended=False # 전송여부 : Message 모델의 sendType이 ALL일 경우 수동으로 크로샷까지 보내야 True로 변경(텔레그램만 전송한 경우 False 유지)
                        )
        except Exception as e:
            print("최종 종료 지역 메시지 생성:", str(e))
            raise Exception("measuring_end/message_end_last: %s" % e)

        # 반환값에 대해서는 향후 고민 필요  //  일단 생성된 종료 message 내용 반환
        return_value = {'result': 'ok'}
        return return_value



########################################################################################################################
# 측정 종료 취소 함수
########################################################################################################################
def measuring_end_cancel(phoneGroup):
    """ 해당지역의 측정 종료를 취소하는 함수
      - 파라미터
        . phoneGroup: 단말그룹(PhoneGroup)
      - 반환값: dict {result : 결과값} // 성공 시 결과값 'ok'
    """
    if phoneGroup.active == True:  # 종료되지 않은 지역일 경우
        return_value = {'result' : 'ERROR: 종료되지 않은 지역'}
        return return_value
    else:
        # 해당 단말그룹에 묶여 있는 단말기들을 가져온다.
        try:
            # 1) 해당 단말그룹이 측정종료되며 생성된 메시지 및 측정종료 데이터(MeasuringDayClose)는 따로 삭제하지 않는다
            phone_list = phoneGroup.phone_set.all()
            # message_list = phoneGroup.message_set.all().filter(Q(status='END') | Q(status='END_LAST'))
            # if message_list.exists():
            #     message_list.delete()

            # 2) 측정종료 처리가 완료된 단말그룹과 측정단말의 상태를 다시 활성화 시킨다.
            phoneGroup.active = True # 단말그룹
            phoneGroup.save()
            phone_list.update(active=True) # 측정단말
                         
        except Exception as e:
            return_value = {'result' : 'error'}
            raise Exception("measuring_end_cancel() - 측정종료 취소: %s" % e)
        
        # 반환값 : Dict
        return_value = {'result': 'ok'}
        return return_value


########################################################################################################################
# 단말 그룹 데이터 합치는 함수
########################################################################################################################
def phonegroup_union(phoneGroup1, phoneGroup2):
    """ 폰그룹 2개를 합치는 함수
      - 파라미터
        . phoneGroup1: 기준 단말
        . phoneGroup2: 합쳐질 단말
      - 반환값: dict {result : 결과값} // 성공 시 결과값 'ok'
    """
    # 콜데이터/초데이터의 phone id를 통일 / 메시지 phone id 및 phonegroup id 통일 -> phone 삭제 -> 종료데이터 삭제 -> event_count 합산 -> phonegroup 삭제 -> active 변경
    try:
        # phoneGroup1 : 기존 데이터, phoneGroup2 : 신규 데이터
        phone_list1 = phoneGroup1.phone_set.all()  # 기준이 되는 단말그룹의 phone 추출
        phone_list2 = phoneGroup2.phone_set.all()  # 합쳐질 단말그룹의 phone 추출
        
        for p2 in phone_list2:
            for p1 in phone_list1:
                if p2.phone_no == p1.phone_no:
                    for p2_data in p2.measurecalldata_set.all():
                        p1.update_phone(p2_data)
                        p2_data.phone = p1
                        p2_data.save()
                    p2.measureseconddata_set.all().update(phone_id=p1.id)
                    p2.message_set.all().update(phone_id=p1.id, phoneGroup_id=phoneGroup1.id)
                    p2.delete()
        
        phoneGroup2.measuringdayclose_set.all().delete()
        phoneGroup1.event_count += phoneGroup2.event_count
        phoneGroup2.delete()
        phoneGroup1.active=True
        phoneGroup1.save()

        return_value = {'result' : 'ok'}
    except Exception as e:
        return_value = {'result' : 'error'}
        raise Exception("phonegroup_union() - 단말그룹 결합 함수: %s" % e)
                
    return return_value
    

########################################################################################################################
# 당일 측정을 마감한다.
########################################################################################################################
def measuring_day_close(phoneGroup_list, measdate):
    """당일측정을 마감하는 함수
      - 파라미터
        . phoneGroup_list: active=True인 단말그룹(PhoneGroup) 리스트
        . measdate: 마감하고자 하는 날짜
      - 반환값: dict {result : 결과값} // 성공 시 결과값 'ok'
    """
    # 1) 단말그룹: 상태변경 - 혹시 남아 있는 상태(True)
    # 2) 측정단말: 상태변경 - 혹시 남아 있는 상태(True)
    # 3) 당일 측정마감 데이터 생성 --> 일일 상황보고 자료 활용 가능
    #    - 대상 데이터: 초단위 데이터
    # 4) 당일 측정종료 메시지 생성 (유형: 단문메시지(XMCS))
    
    # Close한 그룹들에 대해 종료 메시지 생성 - PhoneGroup 과 Phone 의 상태는 종료 메시지 생성 함수에서 변경됨
    for phoneGroup in phoneGroup_list:
        measuring_end(phoneGroup)
 
    # 각 단말 그룹들의 종료 데이터(MeasuringDayClose)를 보충
    for phoneGroup in PhoneGroup.objects.filter(ispId='45008', manage=True, active=False, measdate=measdate):
        try:
            md = phoneGroup.measuringdayclose_set.all().last()  # md : "M"easuringDayClose "D"ata // 중복 마감했을 경우 대비 마지막 저장 메시지 Load
    
            # !!--- 초데이터 기반, 데이터 가공 및 저장은 추후 데이터 확정 시 진행 예정 -- !!
            udpJitter = cal_udpJitter(phoneGroup) # 평균 지연시간 계산
            success_rate = cal_success_rate(phoneGroup) # 전송 성공률 계산
            # 접속시간, LTE CA비율은 계산식 확인 후 추후 추가 업데이트 예정
            connect_time = cal_connect_time(phoneGroup)  # 접속시간 계산
            lte_ca = cal_lte_ca(phoneGroup)  # LTE CA비율 계산
            avg_bw = cal_avg_bw_second(phoneGroup)  # 평균 속도(초데이터)
        
            # 계산한 데이터 저장  - 속도/접속시간/CA률 추후 업데이트
            md.udpJitter, md.success_rate = udpJitter, success_rate
            md.save()

            # 일일보고용 메시지 생성(3.22/ 지속 업데이트 예정) - 측정타입(5G/LTE/3G/WiFi/음성)에 따라 메시지 포맷이 달라진다.
            message_report = f"ㅇ {md.userInfo1}({md.morphology})\n"
            if phoneGroup.networkId != 'WiFi':
                message_report += f" - (DL/UL/시도호/전송성공률)\n" + \
                                  f"  .{md.networkId} \"{md.downloadBandwidth}/{md.uploadBandwidth}/{md.total_count}/{md.success_rate}\"\n"
            # 5G일 경우 LTE전환율 추가 - 접속시간은 추후 정확한 계산식 확인 후 업데이트
            if phoneGroup.networkId == '5G':
                message_report += f"※LTE전환율(DL/UL),접속/지연시간\n" + \
                                  f"  .{md.dl_nr_percent}/{md.ul_nr_percent}%,접속시간계산(업데이트예정)/{md.udpJitter}ms"
            # LTE일 경우 CA비율 추가
            elif phoneGroup.networkId == 'LTE':
                message_report += f"※LTE CA비율(%,4/3/2/1)\n" + \
                                  f"  .{lte_ca[0]}/{lte_ca[1]}/{lte_ca[2]}/{lte_ca[3]}"
            # WiFi일 경우 및 음성호일 경우 : 계산식 확인 후 업데이트 예정
            elif phoneGroup.networkId == "WiFi":
                pass

            # 생성한 메시지를 저장한다 : 기존 메시지 있는 경우 Update, 없는 경우 신규 생성
            message_exists = Message.objects.filter(measdate=measdate, status='REPORT', userInfo1=md.userInfo1)
            if message_exists.exists():
                message_exists.update(downloadBandwidth=md.downloadBandwidth, uploadBandwidth=md.uploadBandwidth, message=message_report, updated_at=datetime.now(), sended=False)
            else:
                Message.objects.create(
                    phoneGroup=phoneGroup,
                    phone=None,
                    status='REPORT',  # REPORT : 일일보고용 메시지
                    measdate=measdate,
                    sendType='XMCS',
                    userInfo1=md.userInfo1,
                    phone_no=None,
                    downloadBandwidth=md.downloadBandwidth,
                    uploadBandwidth=md.uploadBandwidth,
                    messageType='SMS',
                    message=message_report,
                    channelId='',
                    sended=False
                )

        except Exception as e:
            print("마감 데이터 계산, 일일보고 메시지 생성:", str(e))
            raise Exception("measuring_day_close/data_calculate and message_report: %s" % e)

    # 일일보고용 메시지를 수합하여 하나로 작성한다
    try:
        if Message.objects.filter(status='REPORT', measdate=measdate).count() != 0:
            message_report_all = '금일 품질 측정 결과를 아래와 같이 보고 드립니다.\n'
            messages = Message.objects.filter(status='REPORT', measdate=measdate).values_list('message')
            for i in range(len(messages)):
                message_report_all += messages[i][0] + "\n"

            # 메시지를 저장한다.  //  메시지가 이미 존재하면 Update, 없으면 신규 생성
            message_all_exists = Message.objects.filter(status='REPORT_ALL', measdate=measdate, updated_at=datetime.now())
            if message_all_exists.exists():
                message_all_exists.update(message=message_report_all)
            else:
                Message.objects.create(
                    phoneGroup=None,
                    phone=None,
                    status='REPORT_ALL',  # REPORT_ALL : 일일보고용 메시지 전체 수합
                    measdate=measdate,
                    sendType='XMCS',
                    userInfo1=None,
                    phone_no=None,
                    downloadBandwidth=None,
                    uploadBandwidth=None,
                    messageType='SMS',
                    message=message_report_all,
                    channelId='',
                    sended=False
                    )
    except Exception as e:
        print("일일보고 메시지 수합, 생성:", str(e))
        raise Exception("measuring_day_close/message_report_all: %s" % e)
    
    # 5G 및 LTE의 커버리지 측정 대상 수를 계산 및 저장한다.  // total_count 컬럼에 대상 수 저장
    measuring_day_close_coverage(measdate)
        
    # 모든 폰그룹들을 inactive 시킨다.
    PhoneGroup.objects.filter(measdate=measdate).update(active=False)
    
    # 반환값은 Front-End에서 요구하는 대로 추후 수정한다.
    return_value = {'result': 'ok'}
    return return_value




# 재마감 함수
def measuring_day_reclose(measdate):
    """해당 날짜 재마감 함수 : 해당 날짜 측정마감 데이터 재생성
      - 파라미터
        . phoneGroup_list: active=True인 단말그룹(PhoneGroup) 리스트
        . measdate: 마감하고자 하는 날짜
      - 반환값: dict {result : 결과값} // 성공 시 결과값 'ok'
    """  
    # 해당날짜 phoneGroup에 대해 데이터 재생성
    for phoneGroup in PhoneGroup.objects.filter(ispId='45008', manage=True, measdate=measdate):
        try:
            md = phoneGroup.measuringdayclose_set.all()  # 마감 데이터 호출
            # serializer로 폰그룹 데이터 불러온다.
            fields = ['center_id', 'morphology_id', 'measdate', 'userInfo1', 'networkId', \
                    'dl_count', 'ul_count', 'dl_nr_count', 'ul_nr_count']
            serializer = PhoneGroupSerializer(phoneGroup, fields=fields)
            # 일부 데이터는 새로 계산한다
            avg_bandwidth = cal_avg_bw_call(phoneGroup)  # 평균속도 계산 -> 초데이터로 변경 필요
            nr_percent = cal_nr_percent(phoneGroup)  # LTE 전환율 계산
            total_count = max(phoneGroup.dl_count + phoneGroup.dl_nr_count, phoneGroup.ul_count + phoneGroup.ul_nr_count) # 총 콜수
            udpJitter = cal_udpJitter(phoneGroup)  # 평균 지연시간 계산  :  추후 정확한 계산식으로 대체 필요 !!
            success_rate = cal_success_rate(phoneGroup)  # 전송 성공률 계산 : 추후 정확한 계산식으로 대체 필요 !!
            connect_time = cal_connect_time(phoneGroup)  # 접속시간 : 추후 정확한 계산식으로 대체 필요 !!
            #md.lte_ca = cal_lte_ca(phoneGroup)  # LTE CA비율 : 추후 정확한 계산식으로 대체 필요 !!
            #md.avg_bw = cal_avg_bw_second(phoneGroup)  # 평균속도(초데이터) : 추후 정확한 계산식으로 대체 필요 !!
            
            # 기존 데이터 삭제 후 새로운 데이터 저장
            md.delete()
            MeasuringDayClose.objects.create(phoneGroup=phoneGroup, \
                                downloadBandwidth=avg_bandwidth['avg_downloadBandwidth'],
                                uploadBandwidth=avg_bandwidth['avg_uploadBandwidth'], \
                                dl_nr_percent=nr_percent['dl_nr_percent'], ul_nr_percent=nr_percent['ul_nr_percent'], \
                                total_count=total_count, \
                                udpJitter=udpJitter, success_rate=success_rate, connect_time=connect_time,
                                **serializer.data)
            # 5G 및 LTE의 커버리지 측정 대상 수를 계산 및 저장한다.  // total_count 컬럼에 대상 수 저장
            measuring_day_close_coverage(measdate)

        except Exception as e:
            print("재마감 데이터 계산, 저장:", str(e))
            raise Exception("measuring_day_reclose/data_calculate : %s" % e)
    
    # 모든 폰그룹들을 inactive 시킬까? - 검토 중
    # PhoneGroup.objects.filter(measdate=measdate).update(active=False)
    
    # 반환값은 Front-End에서 요구하는 대로 추후 수정한다.
    return_value = {'result': 'ok'}
    return return_value


#####################################################################################################################
####### 측정 종료 or 마감 시 필요한 데이터 계산 함수
#######      - 평균 속도(콜데이터, 초데이터) / LTE전환율 / 평균지연시간 / 전송 성공률 / 접속시간 / LTE CA비율 등
#######      - (4.20 추가) 모폴로지 커버리지인 대상 수 계산 함수
#####################################################################################################################
def cal_avg_bw_call(phoneGroup):
    ''' 평균속도 계산 함수 (콜데이터)
     . 파라미터: phoneGroup
     . 반환값: Dict {avg_downloadBandwidth:DL평균값, avg_uploadBandwidth:UL평균값} '''
    phone_list = phoneGroup.phone_set.all()
    qs = MeasureCallData.objects.filter(phone__in=phone_list, testNetworkType='speed').order_by("meastime")
    # DL 평균속도 : DL측정을 안했을 경우 0으로 처리 (calldata에서 downloadbandwidth 존재 유무로 판단)
    qs_dlbw = qs.exclude( Q(networkId='NR') | Q(downloadBandwidth__isnull=True) | Q(downloadBandwidth=0) )
    if qs_dlbw.exists():
        avg_downloadBandwidth = round(qs_dlbw.aggregate(Avg('downloadBandwidth'))['downloadBandwidth__avg'], 1)
    else: avg_downloadBandwidth = 0
    # UL 평균속도 : UL측정을 안했을 경우 0으로 처리 (calldata에서 uploadbandwidth 존재 유무로 판단)
    qs_ulbw = qs.exclude( Q(networkId='NR') | Q(uploadBandwidth__isnull=True) | Q(uploadBandwidth=0) )
    if qs_ulbw.exists():
        avg_uploadBandwidth = round(qs_ulbw.aggregate(Avg('uploadBandwidth'))['uploadBandwidth__avg'], 1)
    else: avg_uploadBandwidth = 0
    return {'avg_downloadBandwidth':avg_downloadBandwidth, 'avg_uploadBandwidth':avg_uploadBandwidth}

def cal_nr_percent(phoneGroup):
    ''' 5G -> LTE 전환율 계산 함수 (콜데이터)
     . 파라미터: phoneGroup
     . 반환값: Dict {dl_nr_percent:DL전환율, ul_nr_percet:UL전환율} '''
    # DL/UL 5G->LTE전환율 : DL/UL 측정이 없을 경우 0으로 처리 (DL/UL 카운트가 0인 경우)
    if phoneGroup.dl_count == 0: dl_nr_percent = 0.0
    else: dl_nr_percent = round((phoneGroup.dl_nr_count / phoneGroup.dl_count * 100), 1)
    if phoneGroup.ul_count == 0: ul_nr_percent = 0.0
    else: ul_nr_percent = round((phoneGroup.ul_nr_count / phoneGroup.ul_count * 100), 1)
    return {'dl_nr_percent': dl_nr_percent, 'ul_nr_percent': ul_nr_percent}

def cal_udpJitter(phoneGroup):
    ''' 평균 지연시간 계산 함수 (초데이터)
     . 파라미터: phoneGroup
     . 반환값 : 평균 지연시간 (float) '''
    # 평균 지연시간 계산  :  testNetworkType이 latency인 데이터들의 udpJitter 평균값
    phone_list = phoneGroup.phone_set.all()
    qs = MeasureSecondData.objects.filter(phone__in=phone_list, testNetworkType='latency').order_by("meastime")  # 초단위 데이터로 바꿔야함
    if qs.filter(udpJitter__isnull=False).exists():  # data에 udpJitter 없으면 0 처리
        udpJitter = round(qs.exclude(udpJitter__isnull=True).aggregate(Avg('udpJitter'))['udpJitter__avg'], 1)
    else: udpJitter = 0.0
    return udpJitter

def cal_success_rate(phoneGroup):
    ''' 전송성공률 계산 함수 (초데이터)
     . 파라미터: phoneGroup
     . 반환값 : 성공률 (float) '''
    # 전송 성공률 계산 : 전체 콜수에서 "전송실패" + "속도저하" 이벤트 발생 건수 비율로 계산 (추후 정확한 계산식 대체 필요)
    md = phoneGroup.measuringdayclose_set.all().last()
    success_rate = round((1 - (Message.objects.filter(phoneGroup=phoneGroup, status='EVENT').filter( \
                            Q(message__contains='전송실패') | Q(message__contains='속도저하')).count() / md.total_count))*100,1)
    return success_rate

###### 접속시간, LTE CA비율, 평균 DL/UL속도 등은 계산식 확인 후 추후 업데이트
def cal_connect_time(phoneGroup):
    return 0

def cal_lte_ca(phoneGroup):
    ''' LTE CA비율 계산 함수 (콜데이터)
     . 파라미터: phoneGroup
     . 반환값: CA비율(list) [4/3/2/1] '''
    phone_list = phoneGroup.phone_set.all()
    md = phoneGroup.measuringdayclose_set.all().last()
    qs = MeasureSecondData.objects.filter(phone__in=phone_list, testNetworkType='speed')
    # s1~s4 earfcn 값 카운트
    # ca_4 = qs.exclude( Q(s4_EARFCN__isnull=True) | Q(s4_EARFCN=0) ).count() / md.total_count # s4는 제외??
    ca_4 = qs.exclude( Q(s3_EARFCN__isnull=True) | Q(s3_EARFCN=0) ).count() / md.total_count
    ca_3 = qs.exclude( Q(s2_dl_earfcn__isnull=True) | Q(s2_dl_earfcn=0) ).count() / md.total_count
    ca_2 = qs.exclude( Q(s1_dl_earfcn__isnull=True) | Q(s1_dl_earfcn=0) ).count() / md.total_count
    lte_ca = [round(ca_4), round(ca_4+ca_3), round(ca_4+ca_3+ca_2), 100]
    return lte_ca
    
def cal_avg_bw_second(phoneGroup):  ## 콜데이터 써도 무방? networkId=NR 체크 필요??  (4.14) -> 업데이트 예정
    ''' 평균속도 계산 함수 (초데이터)
     . 파라미터: phoneGroup
     . 반환값: Dict {avg_downloadBandwidth:DL평균값, avg_uploadBandwidth:UL평균값} '''
    phone_list = phoneGroup.phone_set.all()
    qs = MeasureSecondData.objects.filter(phone__in=phone_list, testNetworkType='speed').order_by("meastime")
    # DL 평균속도 : DL측정을 안했을 경우 0으로 처리 (data에서 downloadbandwidth 존재 유무로 판단)
    qs_dlbw = qs.exclude( Q(downloadBandwidth__isnull=True) | Q(downloadBandwidth=0) )  # Q(networkId='NR')
    if qs_dlbw.exists():
        avg_downloadBandwidth = round(qs_dlbw.aggregate(Avg('downloadBandwidth'))['downloadBandwidth__avg'], 1)
    else: avg_downloadBandwidth = 0
    # UL 평균속도 : UL측정을 안했을 경우 0으로 처리 (data에서 uploadbandwidth 존재 유무로 판단)
    qs_ulbw = qs.exclude( Q(uploadBandwidth__isnull=True) | Q(uploadBandwidth=0) )  # Q(networkId='NR')
    if qs_ulbw.exists():
        avg_uploadBandwidth = round(qs_ulbw.aggregate(Avg('uploadBandwidth'))['uploadBandwidth__avg'], 1)
    else: avg_uploadBandwidth = 0
    return {'avg_downloadBandwidth':avg_downloadBandwidth, 'avg_uploadBandwidth':avg_uploadBandwidth}


# 측정 마감 시 커버리지 대상 수 계산 함수 --> morphology='커버리지'로 계산  // manage=False 인 애들로 할까? 검토중
# total_count에 대상 수를 저장한다.
def measuring_day_close_coverage(measdate):
    ''' 커버리지 대상 수 계산 함수
     . 파라미터: measdate
     . 반환값: Dict {5G : 5G대상 수, LTE : LTE대상 수} '''
    try:
        fivg_coverage_count = PhoneGroup.objects.filter(ispId='45008', morphology__morphology='커버리지', measdate=measdate, networkId='5G').count()
        lte_coverage_count = PhoneGroup.objects.filter(ispId='45008', morphology__morphology='커버리지', measdate=measdate, networkId='LTE').count()
        coverage_count = {'5G':fivg_coverage_count, 'LTE':lte_coverage_count}
        for key, value in coverage_count.items():
            if MeasuringDayClose.objects.filter(measdate=measdate, networkId=key, morphology__morphology='커버리지').exists():
                MeasuringDayClose.objects.filter(measdate=measdate, networkId=key, morphology__morphology='커버리지').update(total_count=value)
            else:
                MeasuringDayClose.objects.create(
                    phoneGroup=None,
                    measdate=measdate,
                    networkId=key,
                    total_count=value,
                    morphology=Morphology.objects.get(morphology='커버리지'),
                )
        return coverage_count
    except Exception as e: # 묶인 center가 없으면 channelId는 None
        raise Exception("measuring_day_close_coverage(): %s" % e)