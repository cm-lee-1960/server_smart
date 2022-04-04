from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from django.db import connection
from django.db.models import Q
from datetime import datetime

from monitor.models import PhoneGroup, Message
from monitor.serializers import PhoneGroupSerializer, MessageSerializer

########################################################################################################################
# REST API 기능
# - 데이터를 조회해서 JSON 형태로 반환한다.
#
#  /vueapp/dashboard                urls.py                           views.py
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
            qs = PhoneGroup.objects.filter(measdate=measdate, ispId='45008', manage=True)
            phoneGroupList = []
            if qs.exists():
                fields = ['id', 'centerName', 'p_measuringTeam', 'userInfo1', 'morphologyName', 'networkId', 'dl_count',
                          'downloadBandwidth', 'ul_count', 'uploadBandwidth', 'nr_percent', 'event_count',
                          'last_updated_dt', 'last_updated_time', 'active',]
                for phoneGroup in qs:
                    serializer = PhoneGroupSerializer(phoneGroup, fields=fields)
                    phoneGroupList.append(serializer.data)

            # 센터별 측정진행 건수를 가져온다.
            cursor = connection.cursor()
            cursor.execute(" SELECT management_center.centerName AS centerName, COUNT(*) AS coun " + \
                                "FROM monitor_phonegroup, management_center " + \
                                "WHERE ( monitor_phonegroup.center_id = management_center.id ) " + \
                                    f"AND monitor_phonegroup.measdate = '{measdate}' " + \
                                    "AND monitor_phonegroup.ispId = '45008' " + \
                                    "AND monitor_phonegroup.manage = true " + \
                                "GROUP BY management_center.centerName "
                           )

            # 가저온 정보를 JSON 객체(centerList)로 작성한다.
            summary = dict((x, y) for x, y in [row for row in cursor.fetchall()])
            total_count = sum(summary.values())
            centerList = [{'centerName': key, 'count': value} for key, value in summary.items()]
            # for i in range(5-len(centerList)):
            #     centerList.append( {'centerName': ' ', 'count': ' '})

        except Exception as e:
            print("ApiPhoneGroupLV:", str(e))
            raise Exception("ApiPhoneGroupLVt: %s" % e)

        # 해당일자 총 측정건수, 센터별 측정건수, 단말그룹 정보를 JSON 데이터로 넘겨준다.
        data = {'total_count': total_count, # 측정 총건수
                'centerList': centerList, # 센터별 측정건ㅅ
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
                # 해당 단말그룹에 대한 모든 메시지를 가져온다.
                qs = Message.objects.filter(phone__phoneGroup_id=phonegroup_id).order_by('-updated_at')
                if qs.exists():
                    # 1) 이벤트 메시지 내역을 가져온다.
                    event_qs = qs.filter(messageType='EVENT')
                    fields = ['id', 'phone_no_sht', 'create_time', 'message', 'sended_time', 'sended', ]
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