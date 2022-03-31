import enum
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from monitor.models import Phone
from analysis.models import MeasPlan, MeasResult,ReportMessage, MeasLastyear5G, MeasLastyearLTE
import pandas as pd
import datetime
from django.db.models import Sum
from .makereport import *

from monitor.models import *
from management.models import *

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect

###########################
#03/31 측정종료 임시 제거 1번
#03/31 메제지 데이터 ajax dict으로


###########################

def ajax_startdata(toDate_str):
    """초기데이터 가져오는 함수"""
    start_dict = {}
    meas_area = {}
    
    print(toDate_str)
    try:
        measuing_count = len(PhoneGroup.objects.filter(measdate = toDate_str, active=1, ispId='45008',manage=1))#KT데이터만 가져온다.
    except:
        measuing_count = 0
        msg = "{} 측정중 값이 없습니다. ".format(toDate_str)
        print(msg)
        
    ##1번 측정종료 확인 내용(현재버전에서는 제거)     
    # try:
    #     end_count = len(PhoneGroup.objects.filter(measdate=toDate_str, active=0, ispId='45008',manage=1))#KT데이터만 가져온다.
    # except:
    #     end_count = 0
    #     msg = "{} 측정종료 값이 없습니다. ".format(toDate_str)
    #     print(msg) 
        
    start_dict['measuing_count'] = measuing_count
    ##1번 start_dict['end_count'] = end_count
    
    # 측정 그룹을 통해 측정 지역을 가져온다.
    try:
        qs = PhoneGroup.objects.filter(measdate=toDate_str, ispId='45008',manage=1).order_by('-center_id')#KT데이터만 가져온다.
    except:
        qs = []
        msg = "{} 지역 값이 없습니다. ".format(toDate_str)
        print(msg)
        
    area_distint = qs.values_list('center_id', flat=True).distinct()
    # 지역아이디 중복제거 ex)[7,7,7,4,4,4,3] -> [7,4,3]
    
    if len(area_distint) != 0:
        for i in area_distint:
            area_measuing_count = PhoneGroup.objects.filter(measdate=toDate_str, center_id=i,active=1, ispId='45008', manage=1).count()
            #1번 area_end_count = PhoneGroup.objects.filter(measdate=toDate_str, center_id=i, active=0, ispId='45008',manage=1).count()
            #result_count = str(area_measuing_count) + '/' + str(area_end_count)
            result_count =  str(area_measuing_count)

            meas_area_name = Center.objects.get(id=i).centerName + "," + Center.objects.get(id=i).centerEngName
            meas_area_count = result_count
            
            meas_area[meas_area_name] = meas_area_count
        
        # 지역이름 리스트에 넣기
        start_dict['meas_area'] = meas_area
    
    else:
        start_dict['meas_area'] = 'nodata'        
   

    return start_dict

def ajax_messagedata(group_id):
    """초기데이터 가져오는 함수"""
    messsage_dict = {}
    message_type = {}
    
    phone_group = PhoneGroup.objects.get(id = group_id)
    phones = phone_group.phone_set.all()
    #message_data = Message.objects.filters(phonegroup_id=group_id)
    try:
        message_data = Message.objects.filter(phone__in=phones)
    except:
        message_data = []
        msg = "{} 메세지가 없습니다. ".format(phone_group.measuringTeam)
        print(msg)
    
    if len(message_data) != 0:
        for data in message_data:
            message_data = [ data.measdate, data.message, data.sended ]
            if data.messageType == 'EVENT':
                message_type['EVENT'] = message_data 
            elif data.messageType == 'SMS' and data.messageType == 'XROSHOT':
                message_type['XROSHOT'] = message_data
            else:
                message_type['TELE'] = message_data
                
        messsage_dict['message'] = message_type
    else:
        
        messsage_dict['message'] = 'nodata'
        
    return messsage_dict