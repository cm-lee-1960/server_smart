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
    try:
        end_count = len(PhoneGroup.objects.filter(measdate=toDate_str, active=0, ispId='45008',manage=1))#KT데이터만 가져온다.
    except:
        end_count = 0
        msg = "{} 측정종료 값이 없습니다. ".format(toDate_str)
        print(msg) 
        
    start_dict['measuing_count'] = measuing_count
    start_dict['end_count'] = end_count
    
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
            area_end_count = PhoneGroup.objects.filter(measdate=toDate_str, center_id=i, active=0, ispId='45008',manage=1).count()
            result_count = str(area_measuing_count) + '/' + str(area_end_count)

            meas_area_name = Center.objects.get(id=i).centerName + "," + Center.objects.get(id=i).centerEngName
            meas_area_count = result_count
            
            meas_area[meas_area_name] = meas_area_count
        
        # 지역이름 리스트에 넣기
        start_dict['meas_area'] = meas_area
    
    else:
        start_dict['meas_area'] = 'nodata'        
   

    return start_dict