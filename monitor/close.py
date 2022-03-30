from email import message
from django.conf import settings
from django.http import HttpResponse
from django.db.models import Max, Min, Avg, Count, Q
from django.db import connection
from .models import Phone, PhoneGroup, MeasureCallData, Message, MeasuringDayClose
from management.models import Center
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
# |  측정종료   |----------->| ㅇS-CXI 1조 5G 서울특별시-수도권 5호선(방화-하남검단산) 측정종료(07:40~10:20, 95콜) |
# └-----∧------ ┘            |   - LTE 전환율(DL/UL, %): 0 / 14                                                    |
#       |                    |   - 속도(DL/UL, Mbps): 1003.8 / 82.5                                                |
#       |                    └------------------------------------------------------------------------------------ ┘
#       |(측정미종료시/
#       | active=True)       status='REPORT'
# ┌ ----┻-------┐            ┌ --------------------------------------------------┐
# |  측정마감   |----┯------>| ㅇ 서울특별시-수도권 5호선(방화-하남검단산)(테마) |
# └------------ ┘    |       |   - (DL/UL/시도호/전송성공률)                     |
#                    |       |    .5G "1003.6/82.3/105/100.0"                    |
#                    |       |   ※ LTE전환율(DL/UL),접속/지연시간                |
#                    |       |    .0.0/12.0%,접속시간계산(업데이트예정)/16.3ms'  |
#                    |       └-------------------------------------------------- ┘
#                    |
#                    |      status='REPORT_ALL'
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
      - 반환값: dict
        . message_id: 메시지ID
        . message: 메시지 내용
    """
    # 해당 단말그룹에 묶여 있는 단말기들을 가져온다.
    try:
        # --------------------------------------------------------------------------------------------------------------
        # 1) 측정종료된 단말그룹에 대한 측정종료 메시지를 생성한다.
        # --------------------------------------------------------------------------------------------------------------
        phone_list = phoneGroup.phone_set.all()
        qs = MeasureCallData.objects.filter(phone__in=phone_list, testNetworkType='speed').order_by("meastime")
        # DL 평균속도
        avg_downloadBandwidth = round(qs.exclude(Q(networkId='NR') | \
                                                 Q(downloadBandwidth__isnull=True) | \
                                                 Q(downloadBandwidth=0) \
                                                 ).aggregate(Avg('downloadBandwidth'))['downloadBandwidth__avg'], 1)
        # UL 평균속도
        avg_uploadBandwidth = round(qs.exclude(Q(networkId='NR') | \
                                               Q(uploadBandwidth__isnull=True) | \
                                               Q(uploadBandwidth=0)
                                               ).aggregate(Avg('uploadBandwidth'))['uploadBandwidth__avg'], 1)

        # DL/UL 5G->LTE전환율
        dl_nr_percent = round((phoneGroup.dl_nr_count / phoneGroup.dl_count * 100), 1)
        ul_nr_percent = round((phoneGroup.ul_nr_count / phoneGroup.ul_count * 100), 1)

        # 총 콜카운트를 가져온다.
        total_count = min(phoneGroup.dl_count, phoneGroup.ul_count)

        # 측정시작 시간과 측정종료 시간을 확인한다.
        meastime_max_min = qs.aggregate(Max('meastime'), Min('meastime'))
        globals().update(meastime_max_min)
        start_meastime = str(meastime__min)[8:10] + ':' + str(meastime__min)[10:12]
        end_meastime = str(meastime__max)[8:10] + ':' + str(meastime__max)[10:12]

        # 메시지를 작성한다.
        message = f"ㅇS-CXI {phoneGroup.measuringTeam} {phoneGroup.networkId} {phoneGroup.userInfo1} " + \
                  f"측정종료({start_meastime}~{end_meastime}, {total_count}콜)\n"

        # 5G의 경우 메시지 내용에 LTE전환율 포함한다.
        if phoneGroup.networkId == '5G':
            message += f"- LTE 전환율(DL/UL, %): {dl_nr_percent} / {ul_nr_percent}\n"
            message += f"- 속도(DL/UL, Mbps): {avg_downloadBandwidth} / {avg_uploadBandwidth}"

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
                phone=None, # 측정단말
                status='END', # 진행상태(POWERON:파워온, START_F:측정첫시작, START_M:측정시작, MEASURING:측정중, END:측정정료)
                measdate=phoneGroup.measdate, # 측정일자
                sendType='ALL', # 전송유형(TELE: 텔레그램, XMCS: 크로샷, ALL: 모두)
                userInfo1=phoneGroup.userInfo1, # 측정자 입력값1
                phone_no=None, # 측정단말 전화번호
                downloadBandwidth=avg_downloadBandwidth, # DL속도
                uploadBandwidth=avg_uploadBandwidth, # UL속도
                messageType='SMS', # 메시지유형(SMS: 메시지, EVENT: 이벤트)
                message=message, # 메시지 내용
                channelId=chatId, # 채널ID
                sended=False # 전송여부 : Message 모델의 sendType이 ALL일 경우 수동으로 크로샷까지 보내야 True로 변경(텔레그램만 전송한 경우 False 유지)
            )
        else:
            message_end = Message.objects.create(
                phone=None, # 측정단말
                status='END', # 진행상태(POWERON:파워온, START_F:측정첫시작, START_M:측정시작, MEASURING:측정중, END:측정정료)
                measdate=phoneGroup.measdate, # 측정일자
                sendType='ALL', # 전송유형(TELE: 텔레그램, XMCS: 크로샷, ALL: 모두)
                userInfo1=phoneGroup.userInfo1, # 측정자 입력값1
                phone_no=None, # 측정단말 전화번호
                downloadBandwidth=avg_downloadBandwidth, # DL속도
                uploadBandwidth=avg_uploadBandwidth, # UL속도
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
        fields = ['center_id', 'morphology_id', 'measdate', 'userInfo1', 'networkId', 'downloadBandwidth', 'uploadBandwidth', 
                'dl_count', 'ul_count', 'dl_nr_count', 'ul_nr_count', 'dl_nr_percent', 'ul_nr_percent', 'total_count']
        serializer = PhoneGroupSerializer(phoneGroup, fields=fields)
        if md.exists():
            # 해당 단말그룹에 대한 측정종료 데이터를 데이터베이스에 저장한다.
            md.update(**serializer.data)
        else:
            # 해당 단말그룹에 대한 측정종료 데이터를 업데이트 한다
            MeasuringDayClose.objects.create(phoneGroup=phoneGroup, **serializer.data)
        
    except Exception as e:
        print("측정종료 메시지 및 데이터 저장: ", str(e))
        raise Exception("measuring_end() - 측정종료 메시지 및 데이터 저장: %s" % e)


    # ------------------------------------------------------------------------------------------------------------------
    # 3) 해당 단말그룹이 당일 측정종료 최종 마지막일 때 당일 측정종료 메시지를 생성한다.
    # ------------------------------------------------------------------------------------------------------------------
    try:
        # 더 이상 활성화된 단말그룹이 없다면 최종 마지막 단말그룹이라고 판단한다.
        # 즉, 가장 마지막 측정종료 단말그룹이라는 것을 의미한다.
        if PhoneGroup.objects.filter(measdate=phoneGroup.measdate, ispId=45008, active=True).count() == 0:
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

            # 메시지를 생성한다.
            message_end_last = f"금일({daily_day}) S-CXI 품질 측정이 {end_meastime}분에 " + \
                        f"{phoneGroup.userInfo1}({phoneGroup.networkId}{phoneGroup.morphology})을 마지막으로 종료 되었습니다.\n" + \
                        f"ㅇ 측정지역({total_count})\n" + \
                        f" - 5G품질({fiveg_count})\n" + "  .\n" + \
                        f" - LTE/3G 취약지역 품질({lte_count + threeg_count})\n" + "  .\n" + \
                        f" - WiFi 품질({wifi_count})\n" + "  .\n" + \
                        "수고 많으셨습니다."

            # 마지막 종료 메시지가 존재하면 update, 미존재면 신규생성
            message_last_exists = Message.objects.filter(measdate=phoneGroup.measdate, status='END_LAST')
            if message_last_exists.exists():
                message_last_exists.delete()  # 메시지는 생성될 때에만 전송되기때문에 이전 메시지는 삭제
                message_last_exists = Message.objects.create(
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
    return_value = {'message': message}

    return return_value


########################################################################################################################
# 당일 측정을 마감한다.
########################################################################################################################
def measuring_day_close(phoneGroup_list, measdate):
    """당일측정을 마감하는 함수
      - 파라미터
        . phoneGroup_list: active=True인 단말그룹(PhoneGroup) 리스트
        . measdate: 마감하고자 하는 날짜
      - 반환값: string
        . message_report: 일일보고용 메시지 내용
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
    for phoneGroup in PhoneGroup.objects.filter(ispId='45008', active=False, measdate=measdate):
        try:
            phone_list = phoneGroup.phone_set.all()
            qs = MeasureCallData.objects.filter(phone__in=phone_list, testNetworkType='speed').order_by("meastime") # 초데이터로 바꿔야함
            md = phoneGroup.measuringdayclose_set.all().last()  # md : "M"easuringDayClose "D"ata // 중복 마감했을 경우 대비 마지막 저장 메시지 Load
    
            # !!--- 초데이터 기반, 데이터 가공 및 저장은 추후 데이터 확정 시 진행 예정 -- !!
            # 1) 평균 지연시간 계산  :  추후 정확한 계산식으로 대체 필요 !!!(3.22)
            udpJitter = round(qs.exclude( Q(networkId='NR') | \
                                        Q(downloadBandwidth=0) | \
                                        Q(uploadBandwidth=0)
                                        ).aggregate(Avg('udpJitter'))['udpJitter__avg'],1)
            # 2) 전송 성공률 계산 : 전체 콜수에서 "전송실패" 이벤트 발생 건수 비율로 계산 (추후 정확한 계산식 대체 필요)
            success_rate = round((1 - (Message.objects.filter(phone__in=phone_list, message__contains='전송실패').count() / md.total_count))*100,1)
            # 3) 접속시간, LTE CA비율, 평균 DL/UL속도 등은 계산식 확인 후 추후 업데이트
        
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
            # LTE일 경우 CA비율 추가 - CA비율은 추후 정확한 계산식 확인 후 업데이트
            elif phoneGroup.networkId == 'LTE':
                message_report += f"※LTE CA비율(%,4/3/2/1)\n" + \
                                  f"  .CA비율계산값들(업데이트예정)"
            # WiFi일 경우 및 음성호일 경우 : 계산식 확인 후 업데이트 예정
            elif phoneGroup.networkId == "WiFi":
                pass

            # 생성한 메시지를 저장한다 : 기존 메시지 있는 경우 Update, 없는 경우 신규 생성
            message_exists = Message.objects.filter(measdate=measdate, status='REPORT', userInfo1=md.userInfo1)
            if message_exists.exists():
                message_exists.update(downloadBandwidth=md.downloadBandwidth, uploadBandwidth=md.uploadBandwidth, message=message_report, updated_at=datetime.now(), sended=False)
            else:
                Message.objects.create(
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

    # 반환값은 Front-End에서 요구하는 대로 추후 수정한다.
    return_value = {'measdate': measdate, 'message': message_report_all}

    return return_value
