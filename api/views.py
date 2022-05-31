from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.db.models import Q
from datetime import datetime

from rest_framework.decorators import api_view
from monitor.models import PhoneGroup, Message
from monitor.serializers import PhoneGroupSerializer, MessageSerializer, ChatMemberListSerializer
from management.models import Center, Morphology, ChatMemberList, MorphologyDetail, PhoneInfo
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
# 단말그룹 리스트 조회 API
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def phonegroup_list(request, measdate):
    # 측정일자가 파라미터로 넘어오지 않는 경우 현재 날짜로 측정일자를 설정한다.
    if measdate is not None:
        # 측정일자에서 데시(-)를 제거한다(2021-11-01 -> 20211101).
        measdate = measdate.replace('-', '')
    else:
        # 측정일자를 널(Null)인 경우 현재 일자로 설정한다.
       measdate = datetime.now().strftime("%Y%m%d")

    try:
        # 해당 측정일자에 대한 단말그룹 정보를 가져온다.
        if request.user.is_superuser:
            qs = PhoneGroup.objects.filter(measdate=measdate, ispId='45008', manage=True).order_by('-last_updated_dt')
        else:
            qs = PhoneGroup.objects.filter(Q(center=request.user.profile.center) | Q(center_id=1), measdate=measdate, \
                                           ispId='45008', manage=True).order_by('-last_updated_dt')
        phoneGroupList = []
        if qs.exists():
            fields = ['id', 'measdate', 'centerName', 'measuringTeam', 'p_measuringTeam', 'phone_list', 'userInfo1',
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
                " AND monitor_phonegroup.ispId = '45008' " + \
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
        	"               WHERE ispId = '45008' " + \
        	"	                AND manage = True " + \
        	f"	                AND measdate = '{measdate}' " + \
        	"               GROUP BY measuringTeam " + \
            "           ) AS measuringTeam "
        )
        if cursor.rowcount >= 0:
            measuringTeam_count = cursor.fetchall()[0][0]

    except Exception as e:
        print("phonegroup_list():", str(e))
        db_logger.error("phonegroup_list(): %s" % request.user.username)
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

            # DB에서 가저온 메시지 객체의 메시지 내용을 브라우저에서 보내온 변경된 메시지 내용으로 변경한다.
            message.message = message_text
            # message.save()  # 메시지 수정 시 메시지 내용 DB에 업데이트

            # 1) 문자 메시지를 전송한다.
            if sendType == 'XMCS' or sendType == 'ALL':
                from message.xmcs_msg import send_sms_queryset
                receiver_list = receiver_list.replace(' ','').replace('\n','').split(',')
                result_sms = send_sms_queryset(message, receiver_list)
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