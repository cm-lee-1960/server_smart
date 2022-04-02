from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView
from django.db import connection
from datetime import datetime
import json

from monitor.models import PhoneGroup
from monitor.serializers import PhoneGroupSerializer

########################################################################################################################
# 단말그룹 정보를 제공하는 API
# ----------------------------------------------------------------------------------------------------------------------
########################################################################################################################
# Create your views here.
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
                for phoneGroup in qs:
                    fields = ['id', 'centerName', 'p_measuringTeam', 'userInfo1', 'morphologyName', 'networkId', 'dl_count',
                              'downloadBandwidth', 'ul_count', 'uploadBandwidth', 'nr_percent', 'event_count',
                              'last_updated_dt',
                              'active']
                    serializer = PhoneGroupSerializer(phoneGroup)
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
            for i in range(5-len(centerList)):
                centerList.append( {'centerName': ' ', 'count': ' '})

        except Exception as e:
            print("ApiPhoneGroupLV:", str(e))
            raise Exception("ApiPhoneGroupLVt: %s" % e)

        # 해당일자 총 측정건수, 센터별 측정건수, 단말그룹 정보를 JSON 데이터로 넘겨준다.
        data = {'total_count': total_count, 'centerList': centerList, 'phoneGroupList': phoneGroupList}

        return JsonResponse(data=data, safe=False)


