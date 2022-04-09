from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, CreateView
from django.db import connection
from django.db.models import Q
from django.db import models
from datetime import datetime
import json

from monitor.models import PhoneGroup, Message
from monitor.serializers import PhoneGroupSerializer, MessageSerializer
from message.tele_msg import TelegramBot

########################################################################################################################
# REST API 기능
# - 데이터를 조회해서 JSON 형태로 반환한다.
#
#  /vueapp/dashboard                urls.py                            views.py
# ┌---------------------┐           ┌----------------------┐           ┌----------------------┐
# |      홈 페이지      |   ┌------>|         /api         |   ┌------>|         /api         |----┐
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
#
########################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------
# 단말그룹 리스트 조회 API
# ----------------------------------------------------------------------------------------------------------------------
class ApiPhoneGroupLV(ListView):
    model = PhoneGroup
    # 반환값이 JSON 데이터이기 때문에 템플릿 지정이 필요 없다.
    # template_name = ''
    def get(self, request, *args, **kwargs):
        # 측정일자가 파라미터로 넘어오지 않는 경우 현재 날짜로 측정일자를 설정한다.
        if 'measdate' in kwargs.keys():
            s = kwargs['measdate']
            measdate = s[0:4] + s[5:7] + s[8:10]
        else:
           measdate = datetime.now().strftime("%Y%m%d")
        # print(measdate)
        try:
            # 해당 측정일자에 대한 단말그룹 정보를 가져온다.
            qs = PhoneGroup.objects.filter(measdate=measdate, ispId='45008', manage=True).order_by('-last_updated_dt')
            phoneGroupList = []
            if qs.exists():
                fields = ['id', 'centerName', 'p_measuringTeam', 'userInfo1', 'morphologyName', 'networkId', 'dl_count',
                          'downloadBandwidth', 'ul_count', 'uploadBandwidth', 'nr_percent', 'event_count',
                          'last_updated_dt', 'last_updated_time', 'elapsed_time', 'active',]
                for phoneGroup in qs:
                    serializer = PhoneGroupSerializer(phoneGroup, fields=fields)
                    data = serializer.data
                    data['selected'] = False
                    phoneGroupList.append(data)

            # 센터별 측정진행 건수를 가져온다.
            # cursor = connection.cursor()
            # cursor.execute(" SELECT management_center.centerName AS centerName, COUNT(*) AS coun " + \
            #                     "FROM monitor_phonegroup, management_center " + \
            #                     "WHERE ( monitor_phonegroup.center_id = management_center.id ) " + \
            #                         f"AND monitor_phonegroup.measdate = '{measdate}' " + \
            #                         "AND monitor_phonegroup.ispId = '45008' " + \
            #                         "AND monitor_phonegroup.manage = true " + \
            #                     "GROUP BY management_center.centerName "
            #                )
            #
            # # 가저온 정보를 JSON 객체(centerList)로 작성한다.
            # summary = dict((x, y) for x, y in [row for row in cursor.fetchall()])
            # total_count = sum(summary.values())
            # centerList = [{'centerName': key, 'count': value} for key, value in summary.items()]
            #
            # for i in range(5-len(centerList)):
            #     centerList.append( {'centerName': ' ', 'count': ' '})

            # 2022.04.07 - 측정중인 건수와 측정종료된 건수를 확인하기 위해서 다시 작성함
            centerList = []
            total_count = 0
            cursor = connection.cursor()
            cursor.execute(
                    " SELECT management_center.centerName AS centerName, COUNT( * ) AS count, " + \
                    " CAST(SUM(IF(monitor_phonegroup.active = true, 0, 1)) AS UNSIGNED) AS end_count, " + \
                    " CAST(SUM(IF(monitor_phonegroup.active = true, 1, 0)) AS UNSIGNED) AS measuring_count " + \
                    " FROM monitor_phonegroup, management_center " + \
                    " WHERE ( monitor_phonegroup.center_id = management_center.id ) " + \
                    f" AND monitor_phonegroup.measdate = '{measdate}' " + \
                    " AND monitor_phonegroup.ispId = '45008' " + \
                    " AND monitor_phonegroup.manage = true " + \
                    " GROUP BY management_center.centerName "
                )
            for centerInfo in cursor.fetchall():
                centerList.append(
                    {'centerName': centerInfo[0], # 센터명
                     'count': centerInfo[1], # 총 측정건수
                     'end_count': centerInfo[2], # 측정종료 건수
                     'measuring_count': centerInfo[3], # 측정중인 건수
                     })
                total_count += centerInfo[1]

        except Exception as e:
            print("ApiPhoneGroupLV:", str(e))
            raise Exception("ApiPhoneGroupLVt: %s" % e)

        # 해당일자 총 측정건수, 센터별 측정건수, 단말그룹 정보를 JSON 데이터로 넘겨준다.
        data = {'total_count': total_count, # 측정 총건수
                'centerList': centerList, # 센터별 측정건수
                'phoneGroupList': phoneGroupList} # 단말그룹 리스트

        return JsonResponse(data=data, safe=False)

# ----------------------------------------------------------------------------------------------------------------------
# 단말그룹 리스트 조회 API
# ----------------------------------------------------------------------------------------------------------------------
class ApiMessageLV(ListView):
    model = Message

    # 메시지 내역을 조회한다.
    def get(self, request, *args, **kwargs):
        data = {}
        # 조회하고자 하는 메시지ID가 파라미터로 넘어 왔는지 확인한다.
        if 'phonegroup_id' in kwargs.keys():
            phonegroup_id = kwargs['phonegroup_id']

            messageEventList = [] # 이벤트 메시지
            messageSmsList = [] # 문자 메시지
            messageTeleList = [] # 텔레그램
            try:
                # 단말그룹에 대한 측정일자를 조회한다(단말그룹을 찾지 못하는 경우는 당일을 지정한다).
                qs = PhoneGroup.objects.filter(id=phonegroup_id)
                if qs.exists():
                    measdate = qs[0].measdate
                else:
                    measdate = datetime.now().strftime("%Y%m%d")

                # 해당 단말그룹에 대한 모든 메시지를 가져온다.
                qs = Message.objects.filter(
                    Q(phone__phoneGroup_id=phonegroup_id) | \
                    Q(measdate=measdate, sendType='ALL')).order_by('-updated_at')
                if qs.exists():
                    # 1) 이벤트 메시지 내역을 가져온다.
                    event_qs = qs.filter(messageType='EVENT')
                    fields = ['id', 'phone_no_sht', 'create_time', 'message', 'sended_time', 'sended', 'sendType',
                              'telemessageId', 'channelId', 'isDel']
                    if event_qs.exists():
                        for message in event_qs:
                            serializer = MessageSerializer(message, fields=fields)
                            messageEventList.append(serializer.data)

                    # 2) 문자 메시지 내역을 가져온다.
                    sms_qs = qs.filter(Q(sendType='XMCS') | Q(sendType='ALL'))
                    # print("#### SMS", sms_qs.count(), phonegroup_id)
                    if sms_qs.exists():
                        for message in sms_qs:
                            serializer = MessageSerializer(message, fields=fields)
                            messageSmsList.append(serializer.data)

                    # 3) 텔레그램 메시지 내역을 가져온다.
                    tele_qs = qs.filter(sendType='TELE')
                    if tele_qs.exists():
                        for message in tele_qs:
                            serializer = MessageSerializer(message, fields=fields)
                            messageTeleList.append(serializer.data)

                # 클라이언트 브라우저에 전송할 데이터를 랩필한다.
                data = {'messageEventList': messageEventList, # 이벤트 메시지 리스트
                        'messageSmsList': messageSmsList, # 문자 메시지 리스트
                        'messageTeleList': messageTeleList,} # 텔레그램 메시지 리스트

            except Exception as e:
                print("ApiMessageLV:", str(e))
                raise Exception("ApiMessageLV: %s" % e)

        return JsonResponse(data=data, safe=False)


# ----------------------------------------------------------------------------------------------------------------------
# 단말그룹 리스트 조회 API
# ----------------------------------------------------------------------------------------------------------------------
class ApiMessageDV(ListView):
    model = Message

    # 메시지 내역을 조회한다.
    def get(self, request, *args, **kwargs):
        data = {}
        message_id = kwargs['message_id']
        print("##### message id:", message_id)
        qs = Message.objects.filter(id=message_id)
        if qs.exists():
            try:
                bot = TelegramBot()
                message = qs[0]
                print(f"channelId: {message.channelId}, telemessageId: {message.telemessageId}")
                # 전송된 메시지를 취소한다.
                data = bot.delete_message(message.channelId, message.telemessageId)
                # ##### message id: 158
                # channelId: -736183270, telemessageId: 23052
                # ApiMessageDV: Message to delete not found
                # 메시지 회수가 완료되면 회수여부를 업데이트 한다.
                message.isDel = True
                message.save()

            except Exception as e:
                # 오류 코드 및 내용을 반환한다.
                print("ApiMessageDV:", str(e))
                raise Exception("ApiMessageDV: %s" % e)

        return JsonResponse(data=data, safe=False)




# ----------------------------------------------------------------------------------------------------------------------
# 문자 메시지를 전송하는 API
# ----------------------------------------------------------------------------------------------------------------------
def sendMmessage(request, *args, **kwargs):
    data = json.loads(request.body)
    result = {}
    try:
        if request.method == 'POST' and 'sendType' in data.keys():
            sendType = data['sendType'] # 전송유형(sendType)
            receiver_list = data['receiver_list'] # 수신자 리스트
            message = data['message'] # 메시지 내용
            channelId = data['channelId'] # 채널ID
            id = data['id'] # 메시지ID

            if sendType == 'XMCS' or sendType == 'ALL':
                from message.xmcs_msg import send_sms
                result_sms = send_sms(message, receiver_list)
                result = {'result': result_sms}
            elif sendType == 'TELE':
                bot = TelegramBot()
                result = bot.send_message_bot(channelId, message)
                qs = Message.objects.filter(id=id)
                if qs.exists():
                    message = qs[0]
                    message.telemessageId = result['message_id'] # 텔레그램 메시지ID
                    message.sendTime = datetime.now() # 전송시간(보낸시간)
                    message.isDel = False # 메시지 회수여부

                    # 메시지를 저장한다.
                    message.save()

    except Exception as e:
        # 오류 코드 및 내용을 반환한다.
        print("sendMmessage():", str(e))
        raise Exception("sendMmessage(): %s" % e)

    print("##### sendMmessage() 정상처리")

    # return JsonResponse(data=result, safe=False)
    return HttpResponse(result)

# ----------------------------------------------------------------------------------------------------------------------
# 단말그룹 측정조를 변경하는 API
# ----------------------------------------------------------------------------------------------------------------------
def updatePhoneGroup(request, *args, **kwargs):
    data = json.loads(request.body)
    result = {}
    try:
        if request.method == 'POST':
            phoneGroup_id = data['phoneGroup_id']  # 단말그룹ID
            measuringTeam = data['measuringTeam']
            print("##### updatePhoneGroup:", phoneGroup_id, measuringTeam)
            qs = PhoneGroup.objects.filter(id=phoneGroup_id)
            if qs.exists():
                phoneGroup = qs[0]
                phoneGroup.measuringTeam = measuringTeam
                phoneGroup.save()

    except Exception as e:
        # 오류 코드 및 내용을 반환한다.
        print("sendMmessage():", str(e))
        raise Exception("sendMmessage(): %s" % e)

    return HttpResponse(result)