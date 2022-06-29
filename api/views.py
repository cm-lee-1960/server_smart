from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.db.models import Q
from django.shortcuts import render
from datetime import datetime

from rest_framework.decorators import api_view
from monitor.models import PhoneGroup, Message, MeasuringDayClose
from monitor.serializers import PhoneGroupSerializer, MessageSerializer, ChatMemberListSerializer, MeasuringDayCloseSerializer
from monitor.close import cal_close_data, make_report_message
from management.models import Center, Morphology, ChatMemberList, MorphologyDetail, PhoneInfo, MessageConfig
from message.tele_msg import TelegramBot, update_members, update_members_allchat, ban_member_as_compared_db, ban_member_not_allowed, ban_member_not_allowed_all
from monitor.geo import make_map_locations

# 디버깅을 위한 로그를 선언한다.
import logging
db_logger = logging.getLogger('db')

########################################################################################################################
# REST API 기능
# - 데이터를 조회해서 JSON 형태로 반환한다.
#
#  /vueapp/dashboard                urls.py                            views.py
# ┌---------------------┐           ┌----------------------┐           ┌----------------------┐
# |      홈 페이지      |   ┌------>|         /api         |   ┌------>|        APIView       |----┐
# |(dashboard_form.html)|   |       |(smartproject/urls.py)|   |       |    (api/views.py)    |    |
# |                     |   |       └----------┳-----------┘   |       └----------------------┘    |
# |  ┌ ------------┐    |   |                  |               |       - ApiPhoneGroupLV           |
# |  |   Vue.js    |----┼---┘       ┌----------∨-----------┐   |       - ApiMessageLV              |
# |  └-------------┘<---┼---┐       |/api/phonegroup/list  |   |                                   |
# | -async fetch_all_phoneGroup()   |   (api/urls.py)      |---┘                                   |
# └---------------------┘   |       └----------------------┘                                       |
#                           |                                          JsonResponse                |
#                           └----------------------------------------------------------------------┘
# ----------------------------------------------------------------------------------------------------------------------
# 2022.04.03 - 메시지 리스트 조회 API 추가
# 2022.04.07 - 센터별 측정중인 건수와 측정종료 건수를 확인하기 위한 항목을 추가함
# 2022.04.08 - 메시지 전송 및 회수 모듈 추가, 단말그룹 조회시 정열 순서 지정
# 2022.04.09 - 문자 메시지의 경우 단말그룹이 지정되지 않아도 해당 측정일자와 동일한 모든 데이터를 조회하게 함
#            - 텔레그램 메시지 재전송 후 텔레그램 메시지ID, 전송시간(보낸시간), 회수여부(초기화) 항목 업데이트 코드 추가
#            - 텔레그램 메시지 회수 후 회수여부 항목 업데이트 코드 추가
#           ** 메시지 전송/회수 시 메시지 모델에 업데이트 하는 코드를 해당 전담모듈(tele_msg.py)에서 했으면 좋겠는데,
#              메시지 모델(monitor/models.py)와 순환참조가 발생하는 구조라서 불가함
#           ** Message - post_save(SIGNAL) - TelegramBot
#                                            (여기에 업데이트 코드를 넣으면) - Message 구조가 되어 순환참조 발생
#           ** 전송된 메시지를 회수하는 경우는 많지 않으니 현재 구조를 유지해도 괜찮을 듯 함(다소 불편감은 있지만,..)
# 2022.04.10 - 단말그룹에 대한 측정조를 변경하는 기능 추가
#            - 기존 Django View를 REST Framework APIView로 변경 (API 취지에 맞게 수정)
# 2022.05.01 - 측정시작시간 필드 및 문자 메시지 미전송여부 항목(Decorator) 추가
#            - 문자 메시지 전송여부 속성(데코레이터) 항목 추가
#            - DL/UL LTE전환 건수 표기
# 2022.05.10 - 운용본부 및 현장 사용자 계정에 따라 데이터 필터링 기능 추가
#            - 운용본부: superuser
#            - 현장 운용센터: staff
# 2022.05.12 - 측정단말에 대한 사전정보(측정조)가 등록되지 않은 경우 신규 등록하고, 변경된 경우 업데이트 하는 기능 추가
#
########################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------
## IP 정책 함수
# ----------------------------------------------------------------------------------------------------------------------
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     # db_logger.error(request.META)
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


# ----------------------------------------------------------------------------------------------------------------------
# 단말그룹 리스트 조회 API
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def phonegroup_list(request, measdate):
    # 측정일자가 파라미터로 넘어오지 않는 경우 현재 날짜로 측정일자를 설정한다.
    if measdate is not None:
        # 측정일자에서 데시(-)를 제거한다(2021-11-01 -> 20211101).
        measdate = measdate.replace('-', '')
        # IP확인
        #db_logger.error("phonegroup_list():" + request.user.username + " / " + request.META.get('REMOTE_ADDR'))
    else:
        # 측정일자를 널(Null)인 경우 현재 일자로 설정한다.
       measdate = datetime.now().strftime("%Y%m%d")
    
    # db_logger.error(get_client_ip(request))
    # # get_client_ip(request)

    try:
        # 해당 측정일자에 대한 단말그룹 정보를 가져온다.
        if request.user.is_superuser:
            qs = PhoneGroup.objects.filter(measdate=measdate, manage=True).order_by('-last_updated_dt')
        else:
            qs = PhoneGroup.objects.filter(Q(center=request.user.profile.center) | Q(center_id=1), measdate=measdate, \
                                           manage=True).order_by('-last_updated_dt')
        phoneGroupList = []
        if qs.exists():
            fields = ['id', 'measdate', 'centerName', 'measuringTeam', 'p_measuringTeam', 'phone_list', 'userInfo1', 'userInfo2',
                      'starttime', 'morphologyName', 'morphologyDetailId', 'morphologyDetailNetwork', 'morphologyDetailMain', 'morphologyDetailMiddle',
                      'networkId', 'dl_count', 'downloadBandwidth', 'ul_count', 'uploadBandwidth', 'nr_percent',
                      'last_updated_dt', 'last_updated_time', 'elapsed_time', 'active', 'xmcsmsg_sended',
                      'dl_nr_count', 'ul_nr_count', 'dl_nr_count_z', 'ul_nr_count_z',
                      'event_count', 'send_failure_dl_count_z', 'send_failure_ul_count_z', 'all_count_event',]
            for phoneGroup in qs:
                serializer = PhoneGroupSerializer(phoneGroup, fields=fields)
                data = serializer.data
                data['selected'] = False
                # data['failEventCount'] = Message.objects.filter(messageType='EVENT', message__contains='전송실패', measdate=measdate, \
                #                                                         phoneGroup_id=phoneGroup.id).count()  # 전송실패 이벤트 건수
                phoneGroupList.append(data)
                # print(data)

        # 2022.04.07 - 측정중인 건수와 측정종료된 건수를 확인하기 위해서 다시 작성함
        centerList = []
        total_count = 0
        cursor = connection.cursor()
        sql =  " SELECT management_center.centerName AS centerName, COUNT( * ) AS count, " + \
                " CAST(SUM(IF(monitor_phonegroup.active = true, 0, 1)) AS UNSIGNED) AS end_count, " + \
                " CAST(SUM(IF(monitor_phonegroup.active = true, 1, 0)) AS UNSIGNED) AS measuring_count " + \
                " FROM monitor_phonegroup, management_center " + \
                " WHERE ( monitor_phonegroup.center_id = management_center.id ) " + \
                f" AND monitor_phonegroup.measdate = '{measdate}' " + \
                " AND monitor_phonegroup.manage = true "
        # 관리자가 아닌 경우(현장 운용센터 사용자) 해당 운영센터 데이터만 조회할 수 있도록 한다.
        if request.user.is_superuser:
            pass
        else:
            sql += f"AND (center_id = {request.user.profile.center_id} OR  center_id = 1) "
        sql += " GROUP BY management_center.centerName "
        cursor.execute(sql)
        for centerInfo in cursor.fetchall():
            centerList.append(
                {'centerName': centerInfo[0], # 센터명
                 'count': centerInfo[1], # 총 측정건수
                 'end_count': centerInfo[2], # 측정종료 건수
                 'measuring_count': centerInfo[3], # 측정중인 건수
                 })
            total_count += centerInfo[1]

        # 측정조 건수에 대한 정보를 가저온다.
        measuringTeam_count = 0
        cursor.execute(
            "SELECT COUNT(*) As measuringTeam_count " + \
            "    FROM ( " + \
        	"           SELECT measuringTeam AS count FROM smart.monitor_phonegroup " + \
        	"               WHERE manage = True " + \
        	f"	                AND measdate = '{measdate}' " + \
        	"               GROUP BY measuringTeam " + \
            "           ) AS measuringTeam "
        )
        if cursor.rowcount >= 0:
            measuringTeam_count = cursor.fetchall()[0][0]

    except Exception as e:
        print("phonegroup_list():", str(e))
        db_logger.error("phonegroup_list(): %s %s" % request.user.username, request.META.get('REMOTE_ADDR'))
        raise Exception("phonegroup_list(): %s" % e)

    # 해당일자 총 측정건수, 센터별 측정건수, 단말그룹 정보를 JSON 데이터로 넘겨준다.
    data = {'measuringTeam_count': measuringTeam_count, # 측정조건수
            'total_count': total_count, # 측정 총건수
            'centerList': centerList, # 센터별 측정건수
            'phoneGroupList': phoneGroupList, # 단말그룹 리스트
            }

    return JsonResponse(data=data, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# 모폴로지 리스트 조회 API (04.25)
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def centerANDmorphology_list(request):
    try:
        # 모든 센터 및 모폴로지 추출하여 Json 반환
        centerListAll = list(Center.objects.values_list('centerName', flat=True).order_by('id'))
        morphologyList = list(Morphology.objects.values_list('morphology', flat=True).order_by('id'))
        
        ## 모폴로지 상세 데이터 전달을 위한 Dictionary 생성
        MorphDetailDict = {}
        morphDetails_network = list(dict.fromkeys(MorphologyDetail.objects.values_list('network_type', flat=True).order_by('id')))
        for morphDetail_network in morphDetails_network:
            morphDetails_main = MorphologyDetail.objects.filter(network_type=morphDetail_network).values_list('main_class', flat=True)
            MorphDetailDict[morphDetail_network] = dict.fromkeys(morphDetails_main)
            for morphDetail_main in morphDetails_main:
                morphDetails_middle = MorphologyDetail.objects.filter(network_type=morphDetail_network, main_class=morphDetail_main).values_list('middle_class', 'id')
                morphDetail_middle = {}
                for morphDetail_id in morphDetails_middle:
                    morphDetail_middle[morphDetail_id[0]] = morphDetail_id[1]
                MorphDetailDict[morphDetail_network][morphDetail_main] = morphDetail_middle
                
        data = {'morphologyList': morphologyList, 'centerListAll': centerListAll, 'MorphDetailDict': MorphDetailDict} # 센터 및 모폴로지 리스트
    except Exception as e:
        print("centerANDmorphology_list():", str(e))
        raise Exception("centerANDmorphology_list(): %s" % e)

    return JsonResponse(data=data, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# 메시지 리스트 조회 API
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def message_list(request, phonegroup_id):
        data = {}
        # 조회하고자 하는 메시지ID가 파라미터로 넘어 왔는지 확인한다.
        if phonegroup_id is not None:
            messageEventList = [] # 이벤트 메시지
            messageFailEventList = [] # 전송실패 이벤트 메시지
            messageSmsList = [] # 문자 메시지
            messageTeleList = [] # 텔레그램
            messageSmsAllList = [] # 전체 단말그룹의 메시지
            try:
                # 단말그룹에 대한 측정일자를 조회한다(단말그룹을 찾지 못하는 경우는 당일을 지정한다).
                qs = PhoneGroup.objects.filter(id=phonegroup_id)
                if qs.exists():
                    measdate = qs[0].measdate
                    center = qs[0].center
                else:
                    measdate = datetime.now().strftime("%Y%m%d")
                    center = None

                # 해당 단말그룹에 대한 모든 메시지를 가져온다.
                if request.user.is_superuser:
                    qs = Message.objects.filter(
                        #Q(phone__phoneGroup_id=phonegroup_id) | \
                        #Q(measdate=measdate, sendType='ALL')).order_by('-updated_at')
                        Q(measdate=measdate, phoneGroup_id=phonegroup_id)).order_by('-updated_at')
                else:  # 지역일 경우 해당 지역 메시지만 조회
                    qs = Message.objects.filter(Q(measdate=measdate, phoneGroup_id=phonegroup_id, center=center)).order_by('-updated_at')
             
                if qs.exists():
                    # 1) 이벤트 메시지 내역을 가져온다.
                    event_qs = qs.filter(messageType='EVENT')
                    fields = ['id', 'phone_no_sht', 'create_time', 'message', 'sended_time', 'sended', 'sendType',
                              'telemessageId', 'channelId', 'isDel', 'centerName', ]
                    if event_qs.exists():
                        for message in event_qs:
                            serializer = MessageSerializer(message, fields=fields)
                            messageEventList.append(serializer.data)
                    # 1-2) 전송실패 이벤트 메시지 내역은 별도로 
                    fail_event_qs = qs.filter(messageType='EVENT', message__contains='전송실패')
                    if fail_event_qs.exists():
                        for message in fail_event_qs:
                            serializer = MessageSerializer(message, fields=fields)
                            messageFailEventList.append(serializer.data)

                    # 2) 문자(센터) 메시지 내역을 가져온다.
                    ## 센터 보고용 메시지 추가 (5.12)
                    sms_center_qs = Message.objects.filter(Q(measdate=measdate, center=center, status="REPORT_CENTER")).order_by('-updated_at')
                    if sms_center_qs.exists():
                        for message in sms_center_qs:
                            serializer = MessageSerializer(message, fields=fields)
                            messageSmsList.append(serializer.data)
                    sms_qs = qs.filter(Q(sendType='XMCS') | Q(sendType='ALL'))  # 해당 단말그룹의 메시지를 가져온다.
                    if sms_qs.exists():
                        for message in sms_qs:
                            serializer = MessageSerializer(message, fields=fields)
                            messageSmsList.append(serializer.data)

                    # 3) 텔레그램 메시지 내역을 가져온다.
                    tele_qs = qs.filter(Q(sendType='TELE', messageType='SMS') | Q(sendType='ALL', messageType='SMS'))
                    if tele_qs.exists():
                        for message in tele_qs:
                            serializer = MessageSerializer(message, fields=fields)
                            messageTeleList.append(serializer.data)
                    
                    # 4) 문자(전체) 메시지 내역을 가져온다.
                    sms_all_qs = Message.objects.filter(measdate=measdate).order_by('-updated_at').filter(Q(sendType='XMCS') | Q(sendType='ALL'))
                    if sms_all_qs.exists():
                        for message in sms_all_qs:
                            serializer = MessageSerializer(message, fields=fields)
                            messageSmsAllList.append(serializer.data)

                # 클라이언트 브라우저에 전송할 데이터를 랩필한다.
                data = {'messageEventList': messageEventList, # 이벤트 메시지 리스트
                        'messageFailEventList': messageFailEventList, # 전송실패 이벤트 메시지 리스트
                        'messageSmsList': messageSmsList, # 문자 메시지 리스트
                        'messageTeleList': messageTeleList, # 텔레그램 메시지 리스트
                        'messageSmsAllList': messageSmsAllList,} # 전체 문자 메시지 리스트

            except Exception as e:
                print("message_list():", str(e))
                # db_logger.error("message_list(): %s" % e)
                raise Exception("message_list(): %s" % e)

        return JsonResponse(data=data, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# 텔레그램 메시지를 회수하는 API
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def delete_message(request, message_id):
    data = {}
    # 메시지 내역을 조회한다.
    qs = Message.objects.filter(id=message_id)
    if qs.exists():
        try:
            bot = TelegramBot()
            message = qs[0]
            print(f"message_id: {message_id}, channelId: {message.channelId}, telemessageId: {message.telemessageId}")
            # 전송된 메시지를 취소한다.
            data = bot.delete_message(message.channelId, message.telemessageId)
            # 메시지 회수가 완료되면 회수여부를 업데이트 한다.
            message.telemessageId = None # 텔레그램 메시지ID
            message.sended = False # 메시지 전송여부
            message.isDel = True # 메지시 회수여부
            message.save()

        except Exception as e:
            # 오류 코드 및 내용을 반환한다.
            print("delete_message():", str(e))
            # db_logger.error("delete_message(): %s" % e
            # db_logger.exception(e)
            raise Exception("delete_message(): %s" % e)

    return JsonResponse(data=data, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# 문자 메시지를 전송하는 API
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
def send_message(request):
    data = request.data
    result = {}
    try:
        if 'sendType' in data.keys():
            sendType = data['sendType'] # 전송유형(sendType)
            receiver_list = data['receiver_list'] # 수신자 리스트
            message_text = data['message_text'] # 메시지 내용
            channelId = data['channelId'] # 채널ID
            message_id = data['id'] # 메시지ID
            message = Message.objects.get(id=message_id)
            senderCenter = data['senderCenter']

            # DB에서 가저온 메시지 객체의 메시지 내용을 브라우저에서 보내온 변경된 메시지 내용으로 변경한다.
            message.message = message_text
            # message.save()  # 메시지 수정 시 메시지 내용 DB에 업데이트

            # 1) 문자 메시지를 전송한다.
            if sendType == 'XMCS' or sendType == 'ALL':
                from message.xmcs_msg import send_sms_queryset
                receiver_list = receiver_list.replace(' ','').replace('\n','').split(',')
                result_sms = send_sms_queryset(message, receiver_list, senderCenter)
                result = {'result': result_sms}

            # 2) 텔레그램 메시지를 재전송 한다.
            elif sendType == 'TELE':
                bot = TelegramBot()
                result = bot.send_message_bot(channelId, message.message)
                message.telemessageId = result['message_id'] # 텔레그램 메시지ID
                message.sendTime = datetime.now() # 전송시간(보낸시간)
                message.isDel = False # 메시지 회수여부

                # 메시지를 저장한다.
                message.save()

                result = {'result': 'ok'}

    except Exception as e:
        # 오류 코드 및 내용을 반환한다.
        print("send_message():", str(e))
        # db_logger.error("send_message(): %s" % e)
        # db_logger.exception(e)
        raise Exception("send_message(): %s" % e)

    return JsonResponse(data=result, safe=False)
    #return HttpResponse(result)

# ----------------------------------------------------------------------------------------------------------------------
# 단말그룹 정보를 수정하는 API
# 2022.06.08 - 단말그룹 모폴로지를 수정하는 경우 측정단말의 모폴로지도 함께 업데이트 한다.
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
def update_phonegroup_info(request):
    """ 대쉬보드에서 단말그룹 더블클릭하여 정보 수정할 때 함수
        반환값: {result : 'ok' / 'fail'} """
    data = request.data
    try:
        phoneGroup_id = data['phoneGroup_id']  # 단말그룹ID
        qs = PhoneGroup.objects.filter(id=phoneGroup_id)
        if qs.exists():
            phoneGroup = qs[0]
            if 'centerName' in data.keys() :
                previous_center = phoneGroup.center  # 기존 센터
                phoneGroup.center = Center.objects.filter(centerName=data['centerName'])[0]  # 센터 업데이트
                Message.objects.filter(phoneGroup=phoneGroup, center=previous_center).exclude(status='START_F').update(center=phoneGroup.center)  # 센터 변경될 경우 메시지의 센터도 일괄 변경
            if 'measuringTeam' in data.keys() : phoneGroup.measuringTeam = data['measuringTeam']  # 측정조
            if 'morphologyName' in data.keys() :
                phoneGroup.morphology = Morphology.objects.filter(morphology=data['morphologyName'])[0]  # 모폴로지
                # 측정단말 모폴로지도 함께 변경한다.
                phoneGroup.phone_set.update(morphology=phoneGroup.morphology)
                phoneGroup.manage = Morphology.objects.filter(morphology=data['morphologyName']).values_list('manage', flat=True)[0]  # 모폴로지 값에 따른 Manage 값
            if 'morphologyDetailId' in data.keys() : phoneGroup.morphologyDetail = MorphologyDetail.objects.filter(id=data['morphologyDetailId'])[0]  # 모폴로지 상세
            phoneGroup.save()

            # 측정단말에 대한 사전정보(측정조)가 없거나 다른 경우 역방향 업데이를 한다.
            for phone in phoneGroup.phone_set.all():
                qs = PhoneInfo.objects.filter(phone_no=phone.phone_no)
                if qs.exists():
                    # 1) 해당 측정단말에 대한 사전정보(측정조)가 등록되어 있는 경우 등록된 측정조가 일치하는지 확인한다.
                    #    일치하지 않는 경우 측정단말에 대한 사전정보를 업데이트 한다.
                    phoneInfo = qs[0]
                    if phoneGroup.measuringTeam is not phoneInfo.measuringTeam:
                        phoneInfo.measuringTeam = phoneGroup.measuringTeam
                        phoneInfo.save()
                else:
                    # 2) 해당 측정단말에 대한 사전정보가 등록되어 있지 않은 경우 신규 등록한다.
                    PhoneInfo.objects.create(phone_no=phone.phone_no, networkId=phoneGroup.networkId,
                                             measuringTeam=phoneGroup.measuringTeam)
            result = {'result' : 'ok'}
        else:
          result = {'result' : 'fail'}
    except Exception as e:
        # 오류 코드 및 내용을 반환한다.
        result = {'result' : 'fail'}
        raise Exception("update_morphology(): %s" % e)
    return HttpResponse(result)

# ----------------------------------------------------------------------------------------------------------------------
# 텔레그램 채팅방 멤버 조회 API (04.29)
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def get_chatmembers(request, centerName):  # 현재 채팅방의 채팅멤버 리스트 업데이트 하여 전
    if centerName == 'undefined':  # 폰그룹 미선택 상태로 요청이 왔을 시
        data = {'ChatMembers':'fail'}   # fail : 대쉬보드에서 토스트 팝업 띄우지 않음
    else:
        try:
            if centerName.startswith('ALL'):  # 전체 채팅방에 대한 refresh 요청일 경우 추가 처리
                update_members_allchat()
                centerName = centerName[3:]
            if centerName == 'undefined':    # 폰그룹 미선택 상태로 전체 업데이트 요청이 왔을 시
                data = {'ChatMembers':'pass'}  # pass: 화면 refresh 하지 않음
            else:
                channelId = Center.objects.get(centerName=centerName).channelId
                update_members(channelId, Center.objects.get(centerName=centerName))
                ChatMembers = ChatMemberList.objects.filter(center__centerName=centerName).order_by('id')
                ChatMembersList = []
                if ChatMembers.exists():
                    for ChatMember in ChatMembers:
                        fields = ['id', 'userchatId', 'firstName', 'lastName', 'userName', 'centerName', 'chatId', 'allowed', 'isBot', 'join']
                        serializer = ChatMemberListSerializer(ChatMember, fields=fields)
                        data = serializer.data
                        ChatMembersList.append(data)
                data = {'ChatMembers':ChatMembersList}
        except Exception as e:
            print("get_chatmembers():", str(e))
            raise Exception("get_chatmembers(): %s" % e)
    return JsonResponse(data=data, safe=False)

# ----------------------------------------------------------------------------------------------------------------------
# 텔레그램 채팅방 멤버 강퇴 API(5.2)
# ----------------------------------------------------------------------------------------------------------------------
# 1) 버튼 클릭으로 개별 강퇴
@api_view(['GET'])
def ban_chatmember(request, member_id):
    try:
        member = ChatMemberList.objects.get(id=member_id)
        result = TelegramBot().ban_member(member.chatId, member.userchatId)
        if result == True:
            ChatMemberList.objects.get(id=member_id).delete()  # DB에서 해당 멤버 삭제
    except Exception as e:
        print("ban_chatmember():", str(e))
        raise Exception("ban_chatmember(): %s" % e)
    return JsonResponse(data=result, safe=False)

# 2) 특정 or 전체 센터에 대해서 allowed=False인 멤버 전체 강퇴
@api_view(['GET'])
def ban_center_chatmembers(request, centerName):
    try:
        if centerName == 'ALL':  # 전체 추방 요청일 경우
            result = ban_member_not_allowed_all()  # 전체 채팅방에 대해 진행
        elif centerName == 'undefined':  # 단말그룹 미선택 상태로 요청 시
            result = 'fail'
        else:
            center = Center.objects.get(centerName=centerName)  # 특정 센터에 대한 추방 요청일 경우
            result = ban_member_not_allowed(center)  # 특정 센터만 진행
    except Exception as e:
        result = False
        print("ban_center_chatmembers():", str(e))
        raise Exception("ban_center_chatmembers(): %s" % e)
    return JsonResponse(data=result, safe=False)

# ----------------------------------------------------------------------------------------------------------------------
# 측정데이터 지도맵을 작성하는 API
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def make_map(request, phonegroup_id):
    qs = PhoneGroup.objects.filter(id=phonegroup_id)
    if qs.exists():
        try:
            filename = make_map_locations(qs[0])
            result = {
                'result': 'ok',
                'filename': filename.replace('templates/', ''),
            }
            # print(result)
        except Exception as e:
            print("make_map():", str(e))
            raise Exception("make_map(): %s" % e)
    else:
        result = {
            'result': 'fail',
        }
    return JsonResponse(data=result, safe=False)

# ----------------------------------------------------------------------------------------------------------------------
# 마감 데이터 계산식으로 계산한 데이터 보여주는 API
# ----------------------------------------------------------------------------------------------------------------------
def check_data(request, phonegroup_id):
    pg = PhoneGroup.objects.get(id=phonegroup_id)
    pg_close_all = PhoneGroup.objects.filter(measdate=pg.measdate, manage=True, active=False)
    if not pg_close_all.exists():
        return HttpResponse("종료 처리된 단말 그룹이 없습니다. 종료 처리한 단말 그룹들의 데이터만 보여줍니다.")
    else:
        for pg_i in pg_close_all:
            if pg_i.measuringdayclose_set.all().exists():
                cal_close_data(pg_i)
            else:
                return HttpResponse(f"정상적으로 종료되지 않은 단말 그룹이 있습니다. 다시 종료처리를 해주세요.  :  [ {pg_i.userInfo1} ]")
        md = MeasuringDayClose.objects.filter(measdate=pg.measdate, phoneGroup__in=pg_close_all)

        datum = []
        if md.exists():
            fields = ['id', 'measdate', 'phoneGroup', 'userInfo1', 'userInfo2', 'networkId', 'center', 'morphology', 'downloadBandwidth',
                        'uploadBandwidth', 'dl_count', 'ul_count', 'dl_nr_count', 'ul_nr_count', 'dl_nr_percent',
                        'ul_nr_percent', 'connect_time_dl', 'connect_time_ul', 'connect_time', 'udpJitter', 'total_count',
                        'success_rate', 'ca1_count', 'ca2_count', 'ca3_count', 'ca4_count',
                        'ca1_rate', 'ca2_rate', 'ca3_rate', 'ca4_rate', 'phoneGroup_id',]
            for md_i in md:
                serializer = MeasuringDayCloseSerializer(md_i, fields=fields)
                data = serializer.data
                datum.append(data)
        
        return render(request, 'analysis/show_data.html', {'datum':datum, 'i':phonegroup_id})

# ----------------------------------------------------------------------------------------------------------------------
# 마감 메시지를 간이로 보여주는 API (메시지 모델에 저장은 안함)
# ----------------------------------------------------------------------------------------------------------------------
def check_message(request, phonegroup_id):
    measdate=PhoneGroup.objects.filter(id=phonegroup_id)[0].measdate
    pg_all = PhoneGroup.objects.filter(measdate=measdate, manage=True).order_by('networkId')
    close_message_list = []
    message_end_last = ''

    # 1) 각 단말 그룹에 대한 종료 메시지 생성
    for pg_i in pg_all:  
        md = pg_i.measuringdayclose_set.all()
        if md.exists():
            md = md.last()
            md.add_count = md.dl_count + md.ul_count  # 시도호 (DL카운트 + UL카운트) 

            if pg_i.networkId == 'WiFi':
                message_report = f"ㅇ {md.userInfo1}({md.morphology})\n" + \
                            f" - 속도(DL/UL, Mbps)\n" + \
                            f"  . WiFi({pg_i.morphologyDetail.main_class})\"{md.downloadBandwidth}/{md.uploadBandwidth}\""

            else:
                message_report = f"ㅇ {md.userInfo1}({md.morphology})\n" + \
                                f" - (DL/UL/시도호/전송성공률)\n" + \
                                f"  .{md.networkId} \"{md.downloadBandwidth}/{md.uploadBandwidth}/{md.add_count}/{md.success_rate}\"\n"
                # 5G일 경우 LTE전환율/접속시간 추가
                if pg_i.networkId == '5G':
                    message_report += f"※LTE전환율(DL/UL),접속/지연시간\n" + \
                                    f"  .{md.dl_nr_percent}/{md.ul_nr_percent}%,{md.connect_time}/{md.udpJitter}ms"

            close_message_list.append(message_report)

    # 2) 최종 지역 종료 메시지 생성
    pg_endlast = pg_all.order_by('-last_updated')[0]
    end_meastime = str(pg_endlast.last_updated)[8:10] + ':' + str(pg_endlast.last_updated)[10:12]
    daily_day = str(measdate)[4:6] + '월' + str(measdate)[6:8] + '일'
    cursor = connection.cursor()
    cursor.execute(" SELECT networkId, COUNT(*) AS COUNT " + \
                    "      FROM monitor_phonegroup " + \
                    f"      WHERE measdate='{measdate}' and " + \
                    # "             ispId = '45008' and " + \
                    "             manage = True " + \
                    "      GROUP BY networkId "
                    )
    result = dict((x, y) for x, y in [row for row in cursor.fetchall()])
    fiveg_count = result['5G'] if '5G' in result.keys() else 0 # 5G 측정건수
    lte_count = result['LTE'] if 'LTE' in result.keys() else 0 # LTE 측정건수
    threeg_count = result['3G'] if '3G' in result.keys() else 0 # 3G 측정건수
    wifi_count = result['WiFi'] if 'WiFi' in result.keys() else 0 # WiFi 측정건수
    total_count = fiveg_count + lte_count + threeg_count + wifi_count
    userInfo_byType = {'5G':'', 'LTE':'', '3G':'', 'WiFi':''}
    for userInfo in pg_all.exclude(networkId__isnull=True).values('networkId', 'userInfo1', 'morphologyDetail'):
        userInfo_byType[userInfo['networkId']] += '\n  .' + userInfo['userInfo1']
        if userInfo['networkId'] == 'WiFi':  # WiFi일 경우 상용/공공/개방 구분자 추가
            userInfo_byType[userInfo['networkId']] += '(' + MorphologyDetail.objects.get(id=userInfo['morphologyDetail']).main_class +')'
    message_end_last = f"금일({daily_day}) S-CXI 품질 측정이 {end_meastime}분에 " + \
                f"{pg_endlast.userInfo1}({pg_endlast.networkId}{pg_endlast.morphology})을 마지막으로 종료 되었습니다.\n" + \
                f"ㅇ 측정지역({total_count})\n" + \
                f" - 5G품질({fiveg_count})" + f"{userInfo_byType['5G']}\n" + \
                f" - LTE/3G 취약지역 품질({lte_count + threeg_count})" + f"{userInfo_byType['LTE']}" + f"{userInfo_byType['3G']}\n" + \
                f" - WiFi 품질({wifi_count})" + f"{userInfo_byType['WiFi']}\n" + \
                "수고 많으셨습니다."
    
    # 3) 최종 보고 메시지 생성
    message_report_all = '금일 품질 측정 결과를 아래와 같이 보고 드립니다.'
    for message in close_message_list:
        message_report_all += "\n\n" + message  # 운용본부용 전체 메시지 수합

    closeMessage = {'close_message': close_message_list, 'last_message': message_end_last, 'report_message': message_report_all}       
    return render(request, 'analysis/show_closeMessage.html', closeMessage)


# ----------------------------------------------------------------------------------------------------------------------
# 마감 메시지를 간이로 보여주는 API (메시지 모델에 저장은 안함)
# ----------------------------------------------------------------------------------------------------------------------
def unmanage_pg(request, phonegroup_id):
    try:
        pg = PhoneGroup.objects.get(id=phonegroup_id)
        pg.manage = False
        pg.save()
        return JsonResponse(data={'result':'ok'}, safe=False)
    except:
        return JsonResponse(data={'result':'fail'}, safe=False)

# ----------------------------------------------------------------------------------------------------------------------
# 측정 종료/시작 설정 API  (문자 자동 전송 전체 ON/OFF)
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
def monitoring_condition(request):
    data = request.data
    if data['purpose'] == True:  # 현재 상태 체크 목적으로 POST 요청이 온 경우
        result = {'result' : 'ok', 'status' : MessageConfig.objects.all().values_list('ALL', flat=True)[0]}
    else:  # 측정 상태 변경을 위한 목적으로 POST 요청이 온 경우
        if data['status'] == True:
            MessageConfig.objects.all().update(ALL=False)         # 자동감시(자동메시지 전송) OFF 설정
            result = {'result' : 'ok', 'status' : False}
        else: 
            MessageConfig.objects.all().update(ALL=True)
            result = {'result' : 'ok', 'status' : True}          # 자동감시(자동메시지 전송) ON 설정
    return JsonResponse(data=result, safe=False)



# -------------------------------------------------------------------------------------------------
# 새 메시지 전송 함수
# -------------------------------------------------------------------------------------------------
def new_msg_render(request):   ## 새메시지 전송 HTML
    centerNames = Center.objects.all().values_list('centerName', flat=True)
    return render(request, 'analysis/sendNewmessage.html', {'Centers':centerNames})

@api_view(['POST'])   ## 새메시지 전송 HTML에서 POST 요청을 받아 메시지를 전송하는 함수
def send_new_msg(request):
    data = request.data
    if 'sendType' in data.keys():
        sendType = data['sendType']
        message = data['message']
        if sendType == 'XMCS':
            receiver = data['receiver']
            senderCenter = data['senderCenter']

            from message.xmcs_msg import send_sms, report_sms
            receiver_list = receiver.replace(' ','').replace('\n','').split(',')
            senderNum = Center.objects.filter(centerName=senderCenter)[0].senderNum
            result_sms = send_sms(message, senderNum, receiver_list)
            if result_sms['status_code'] == 200:  # 크로샷 전송 결과 개별 조회 수행 (정상 전송되었는지 확인)
                cnt = result_sms['body']['response']['Count']  # 전송 대상 수
                SendDay = result_sms['body']['response']['SubmitTime'][:8]  # 보낸날짜
                JobIDs = []  # 조회할 개별 JobID 리스트
                for i in range(cnt):
                    JobIDs.append(result_sms['body']['response']['JobIDs'][i]['JobID'])
                result = report_sms(JobIDs, SendDay)  # 조회 결과 : Dict, {수신자번호 : 결과}
                return render(request, 'analysis/sendNewmessageResult.html', result)  # 크로샷 전송 조회 결과를 반환

        elif sendType == 'TELE':
            teleCenter = data['teleCenter']
            channelId = Center.objects.filter(centerName=teleCenter)[0].channelId

            bot = TelegramBot()
            result = bot.send_message_bot(channelId, message)
            return HttpResponse("전송 완료")