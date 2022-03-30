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
        measuing_count = len(PhoneGroup.objects.filter(measdate = toDate_str, active=1, ispId='45008'))#KT데이터만 가져온다.
    except:
        measuing_count = 0
        msg = "{} 측정중 값이 없습니다. ".format(toDate_str)
        print(msg) 
    try:
        end_count = len(PhoneGroup.objects.filter(measdate=toDate_str, active=0, ispId='45008'))#KT데이터만 가져온다.
    except:
        end_count = 0
        msg = "{} 측정종료 값이 없습니다. ".format(toDate_str)
        print(msg) 
        
    start_dict['measuing_count'] = measuing_count
    start_dict['end_count'] = end_count
    
    # 측정 그룹을 통해 측정 지역을 가져온다.
    try:
        qs = PhoneGroup.objects.filter(measdate=toDate_str, ispId='45008').order_by('-center_id')#KT데이터만 가져온다.
    except:
        qs = []
        msg = "{} 지역 값이 없습니다. ".format(toDate_str)
        print(msg)
        
    area_distint = qs.values_list('center_id', flat=True).distinct()
    # 지역아이디 중복제거 ex)[7,7,7,4,4,4,3] -> [7,4,3]
    
    if len(area_distint) != 0:
        for i in area_distint:
            area_measuing_count = PhoneGroup.objects.filter(measdate=toDate_str, center_id=i,active=1, ispId='45008').count()
            area_end_count = PhoneGroup.objects.filter(measdate=toDate_str, center_id=i, active=0, ispId='45008').count()
            result_count = str(area_measuing_count) + '/' + str(area_end_count)

            meas_area_name = Center.objects.get(id=i).centerName
            meas_area_count = result_count
            
            meas_area[meas_area_name] = meas_area_count
        
        # 지역이름 리스트에 넣기
        start_dict['meas_area'] = meas_area
    
    else:
        start_dict['meas_area'] = 'nodata'        
   

    return start_dict

def ajax_phoneGroupData():
    """폰그룹 데이터 가져오는 함수"""
    group_dict = {}
    
    if len(PhoneGroup.objects.all()) != 0:
        for phonegroup in PhoneGroup.objects.filter(ispId='45008'): #KT데이터만 가져온다.
            group_dict_list=[] # 리스트 초기화
            qs = phonegroup.phone_set.all() # 폰그룹으로 폰하위 가져오기 
            
            #. 1. 센터 이름
            center = {}
            center_name = CenterManageArea.objects.filter(siDo=qs[0].siDo, guGun=qs[0].guGun)[0].opCenter
            center['center_name'] = center_name
            #. 2. 그룹 이름
            group = {}
            group_name = phonegroup.measuringTeam
            group['group_name'] = group_name
            #. 3. 단말 번호
            phone = {}
            phone_number_dump = []
            for i in qs:
                phone_number_dump.append(str(i.phone_no)[-4:])
            phone_number = ','.join(phone_number_dump)
            phone['phone_number'] = phone_number
            #. 4.측정지역
            userinfo = {}
            userinfo_name = phonegroup.userInfo1
            userinfo['userinfo_name'] = userinfo_name
            #. 5.모폴로지
            morpology = {}
            morpology_name = Morphology.objects.get(id=phonegroup.morphology_id).morphology
            morpology['morpology_name'] = morpology_name
            #. 6.네트워크
            network = {}
            network_name = phonegroup.networkId
            network['network_name'] = network_name
            #. 7.DL_콜수
            DL_Call = {}
            DL_Call_count = phonegroup.dl_count
            DL_Call['DL_Call_count'] = DL_Call_count
            #. 8.DL_속도
            DL_Th = {}
            DL_Th_dump = 0
            for i in qs:
                DL_Th_dump += (i.downloadBandwidth * i.dl_count)
                
            try:
                DL_Throughput = round((DL_Th_dump / DL_Call_count), 2) #DL카운트 재활용
            except:
                DL_Throughput = '-'
                
            DL_Th['DL_Throughput'] = DL_Throughput
            #. 9.UL_콜수
            UL_Call = {}
            UL_Call_count = phonegroup.ul_count
            UL_Call['UL_Call_count'] = UL_Call_count
            #. 10.DL_속도
            UL_Th = {}
            UL_Th_dump = 0
            for i in qs:
                UL_Th_dump += (i.uploadBandwidth * i.ul_count)
            
            try:
                UL_Throughput = round((UL_Th_dump / UL_Call_count), 2) #DL카운트 재활용
            except:
                UL_Throughput = '-'
                
            UL_Th['UL_Throughput'] = UL_Throughput
            #. 11.LTE전환율
            LTE_Change = {}
            if network_name == '5G':
                NR_count = phonegroup.dl_nr_count + phonegroup.ul_nr_count
                if NR_count == 0:
                    LTE_Change_per = "0%"
                else:
                    LTE_Change_per = str(round(((DL_Call+UL_Call) / NR_count) * 100)) + "%" # 전환율계산
                LTE_Change['LTE_Change_per'] = LTE_Change_per
            else:
                LTE_Change['LTE_Change_per'] = '-'
            #. 12.CA(필요하면 추후에 데이터 가져와야한다.)
            CA_Info = {}
            if network_name == 'LTE':
                CA_Info['CA_num'] = 0
            else:
                CA_Info['CA_num'] = '-'
            #. 13.이벤트 개수
            event = {}
            event_num = 0     
            for i in qs:
                event_num += len(Message.objects.filter(phone_id=i.id, messageType='EVENT'))
            event['event_num'] = event_num
            #. 14.측정시간
            meas_Time = {}
            meastime_dump = []
            for i in qs:
                meastime_dump.append(i.last_updated)
            meastime_dump.sort(reverse=True)
            meastime = str(meastime_dump[0])[8:10] + ":" + str(meastime_dump[0])[10:12] \
                    + ":" + str(meastime_dump[0])[12:14]
            meas_Time['meastime'] = meastime
            #. 14.상태
            active = {}
            if phonegroup.active == 1:
                active['active_name'] = "측정중"
            else:
                active['active_name'] = "종료"
            
            group_dict_list = [center,group,phone,userinfo, \
                            morpology,network,DL_Call, \
                            DL_Th,UL_Call,UL_Th,LTE_Change, \
                            CA_Info,event,meas_Time,active] ## 리스트에 데이터 넣기   
            
            group_dict[str(phonegroup.id)] = group_dict_list ## 딕셔너리에 ID를 키로 최종 데이터넣기
    
    else:
        group_dict['no_data'] = "nodata" 

    return group_dict


# def form_eventdata():