from django.db.models import Avg, Max
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from monitor.models import Phone, MeasuringDayClose
from analysis.models import *
import pandas as pd
import numpy as np
import datetime
from datetime import date, timedelta
from django.db.models import Sum
from django.db.models import Q
###################################################################################################
# 일일보고 및 대상등록 관련 모듈
# -------------------------------------------------------------------------------------------------
# 2022-03-23 - 모듈 정리 및 주석 추가
###################################################################################################

# -------------------------------------------------------------------------------------------------
# 일일보고 페이지
# - 실제 측정마감데이터로 교체(4.19)
#
# [ 고민해야 하는 사항 ]
#  - JSON형태의 컨텍스트를 만드는 코드 정규화
# -------------------------------------------------------------------------------------------------
networkid_list = ["5G NSA", "5G SA", "5G 공동망", "LTE", "WiFi", "품질취약지역"]
district_list = ['서울','인천','부산','울산','대구','광주','대전','경기','강원','경남','경북','전남','전북','충남','충북','세종','고속도로','지하철','전국']

center_list = ['서울강북','강원','경기북부','서울강남','경기남부','경기서부','부산','경남','대구','경북','전남','전북','충남','충북']
city_list = ["대도시",'중소도시','농어촌']
facility5g_list = ['대형점포','대학교','아파트','병원','영화관','공항','거리','시장','지하상가','놀이공원','도서관','전시시설','터미널']
traffic5g_list = ['지하철노선','고속도로','지하철역사','KTX.SRT역사','KTX.SRT노선']
inbuildinglte_list = ['대형점포','KTX.SRT역사','대형병원','터미널','지하철역사','공항','전시시설','지하상가']
themelte_list = ['지하철','전통시장','대학교','놀이공원','주요거리','고속도로','KTX.SRT노선']
center_list1 = ['서울강북','강원','경기북부','서울강남','경기남부','경기서부','부산']
center_list2 = ['경남','대구','경북','전남','전북','충남','충북']
def get_report_cntx(request):
    """ 일일보고 페이지에 보여질 데이터를 조회해서 JSON으로 반환하는 함수
        - 파라미터:
          . year : 해당년도
        - 반환값: context (JSON형태)
    """
   
    #리포트 날짜 추출 및 검색
    
    # if reportdate == "GET" :
    #     reportdate = request.GET.get('reportdate')
    # else : 
    #     reportdate = date.today()
    
    reportdate = request.GET.get('reportdate')
   
    firstday = LastMeasDayClose.objects.last().measdate
    #사후측정 전체
    
    if reportdate is None:
        hodate = date.today()
        reportdate = date.today().strftime('%Y-%m-%d')
       
    else :
        format_data = "%Y-%m-%d"
        hodate = datetime.datetime.strptime(reportdate, format_data).date()    
       
    
    # class comment(LastMeasDayClose):
    #     date = LastMeasDayClose.measdate()
    # class F(FilterSet):
    #     date = DateFromToRangeFilter()
    #     class Meta:
    #         model = comment
    #         fields = ['date']
    
    # f = F({'date_after':firstday, 'date_before':hodate})
    # print(f)

    postmeasure5g = PostMeasure5G.objects.filter(measdate__range=[firstday,hodate])
    postmeasurelte = PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate])
    #사후측정 5G
    postmeas5glist = [] 
    postmeas5grankdllist = []
    postmeas5grankullist = []
    postmeas5g_district = []
    postmeas5g_lastkt_dl = []
    postmeas5g_lastskt_dl = []
    postmeas5g_lastlg_dl = []
    postmeas5g_measkt_dl = []
    postmeas5g_measkt_ul = []
    postmeas5g_measkt_rsrp = []
    postmeas5g_measkt_lte = []
    postmeas5g_postmeaskt_dl = []
    postmeas5g_postmeaskt_ul = []
    postmeas5g_postmeaskt_rsrp = []
    postmeas5g_postmeaskt_lte = []
    postmeas5g_postmeasskt_dl = []
    postmeas5g_postmeasskt_ul = []
    postmeas5g_postmeasskt_rsrp = []
    postmeas5g_postmeasskt_lte = []
    postmeas5g_postmeaslg_dl = []
    postmeas5g_postmeaslg_ul = []
    postmeas5g_postmeaslg_rsrp = []
    postmeas5g_postmeaslg_lte = []
    postmeas5gtotal_district = PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).count()
    try:
        postmeas5gtotal_lastkt_dl = round(MeasLastyeardistrict.objects.get(district = '종합', nettype = '5G').KTDL)
    except:
        postmeas5gtotal_lastkt_dl = ""
    try:
        postmeas5gtotal_lastskt_dl = round(MeasLastyeardistrict.objects.get(district = '종합', nettype = '5G').SKTDL)
    except:
        postmeas5gtotal_lastskt_dl = ""
    try:
        postmeas5gtotal_lastlg_dl = round(MeasLastyeardistrict.objects.get(district = '종합', nettype = '5G').LGDL)
    except:
        postmeas5gtotal_lastlg_dl = ""
    try:
        postmeas5gtotal_measkt_dl = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("measkt_dl"))["measkt_dl__avg"],1)
    except:
        postmeas5gtotal_measkt_dl = ""
    try:
        postmeas5gtotal_measkt_ul = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("measkt_ul"))["measkt_ul__avg"],1)
    except:
        postmeas5gtotal_measkt_ul = ""
    try:
        postmeas5gtotal_measkt_rsrp = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("measkt_rsrp"))["measkt_rsrp__avg"],1)
    except:
        postmeas5gtotal_measkt_rsrp = ""
    try:
        postmeas5gtotal_measkt_lte = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("measkt_lte"))["measkt_lte__avg"],1)
    except:
        postmeas5gtotal_measkt_lte = ""
    try:
        postmeas5gtotal_postmeaskt_dl = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_dl"))["postmeaskt_dl__avg"],1)
    except:
        postmeas5gtotal_postmeaskt_dl = ""
    try:
        postmeas5gtotal_postmeaskt_ul = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_ul"))["postmeaskt_ul__avg"],1)
    except:
        postmeas5gtotal_postmeaskt_ul = ""
    try:
        postmeas5gtotal_postmeaskt_rsrp = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_rsrp"))["postmeaskt_rsrp__avg"],1)
    except:
        postmeas5gtotal_postmeaskt_rsrp = ""
    try:
        postmeas5gtotal_postmeaskt_lte = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_lte"))["postmeaskt_lte__avg"],1)
    except:
        postmeas5gtotal_postmeaskt_lte = ""
    try:
        postmeas5gtotal_postmeasskt_dl = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_dl"))["postmeasskt_dl__avg"],1)
    except:
        postmeas5gtotal_postmeasskt_dl = ""
    try:
        postmeas5gtotal_postmeasskt_ul = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_ul"))["postmeasskt_ul__avg"],1)
    except:
        postmeas5gtotal_postmeasskt_ul = ""
    try:
        postmeas5gtotal_postmeasskt_rsrp = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_rsrp"))["postmeasskt_rsrp__avg"],1)
    except:
        postmeas5gtotal_postmeasskt_rsrp = ""
    try:
        postmeas5gtotal_postmeasskt_lte = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_lte"))["postmeasskt_lte__avg"],1)
    except:
        postmeas5gtotal_postmeasskt_lte = ""
    try:
        postmeas5gtotal_postmeaslg_dl = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_dl"))["postmeaslg_dl__avg"],1)
    except:
        postmeas5gtotal_postmeaslg_dl = ""
    try:
        postmeas5gtotal_postmeaslg_ul = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_ul"))["postmeaslg_ul__avg"],1)
    except:
        postmeas5gtotal_postmeaslg_ul = ""
    try:
        postmeas5gtotal_postmeaslg_rsrp = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_rsrp"))["postmeaslg_rsrp__avg"],1)
    except:
        postmeas5gtotal_postmeaslg_rsrp = ""
    try:
        postmeas5gtotal_postmeaslg_lte = round(PostMeasure5G.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_lte"))["postmeaslg_lte__avg"],1)
    except:
        postmeas5gtotal_postmeaslg_lte = ""
    for i in district_list:
        if PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).count() > 0 :
            postmeas5glist.append(i)
    for i in postmeas5glist:
        
        postmeas5g_district.append((PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate])).count())
        
        try:
            postmeas5g_lastkt_dl.append(round(MeasLastyeardistrict.objects.get(district = i, nettype = '5G').KTDL))
        except:
            postmeas5g_lastkt_dl.append("")
        try:
            postmeas5g_lastskt_dl.append(round(MeasLastyeardistrict.objects.get(district = i,nettype = '5G').SKTDL))
        except:
            postmeas5g_lastskt_dl.append("")
        try:
            postmeas5g_lastlg_dl.append(round(MeasLastyeardistrict.objects.get(district = i,nettype = '5G').LGDL))
        except:
            postmeas5g_lastlg_dl.append("")
        try:
            postmeas5g_measkt_dl.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("measkt_dl"))["measkt_dl__avg"],1))
        except:
            postmeas5g_measkt_dl.append("")
        try:
            postmeas5g_measkt_ul.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("measkt_ul"))["measkt_ul__avg"],1))
        except:
            postmeas5g_measkt_ul.append("")
        try:
            postmeas5g_measkt_rsrp.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("measkt_rsrp"))["measkt_rsrp__avg"],1))
        except:
            postmeas5g_measkt_rsrp.append("")
        try:
            postmeas5g_measkt_lte.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("measkt_lte"))["measkt_lte__avg"],1))
        except:
            postmeas5g_measkt_lte.append("")
        try:
            postmeas5g_postmeaskt_dl.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_dl"))["postmeaskt_dl__avg"],1))
        except:
            postmeas5g_postmeaskt_dl.append("")
        try:
            postmeas5g_postmeaskt_ul.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_ul"))["postmeaskt_ul__avg"],1))
        except:
            postmeas5g_postmeaskt_ul.append("")
        try:
            postmeas5g_postmeaskt_rsrp.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_rsrp"))["postmeaskt_rsrp__avg"],1))
        except:
            postmeas5g_postmeaskt_rsrp.append("")
        try:
            postmeas5g_postmeaskt_lte.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_lte"))["postmeaskt_lte__avg"],1))
        except:
            postmeas5g_postmeaskt_lte.append("")
        try:
            postmeas5g_postmeasskt_dl.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_dl"))["postmeasskt_dl__avg"],1))
        except:
            postmeas5g_postmeasskt_dl.append("")
        try:
            postmeas5g_postmeasskt_ul.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_ul"))["postmeasskt_ul__avg"],1))
        except:
            postmeas5g_postmeasskt_ul.append("")
        try:
            postmeas5g_postmeasskt_rsrp.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_rsrp"))["postmeasskt_rsrp__avg"],1))
        except:
            postmeas5g_postmeasskt_rsrp.append("")
        try:
            postmeas5g_postmeasskt_lte.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_lte"))["postmeasskt_lte__avg"],1))
        except:
            postmeas5g_postmeasskt_lte.append("")
        try:
            postmeas5g_postmeaslg_dl.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_dl"))["postmeaslg_dl__avg"],1))
        except:
            postmeas5g_postmeaslg_dl.append("")
        try:
            postmeas5g_postmeaslg_ul.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_ul"))["postmeaslg_ul__avg"],1))
        except:
            postmeas5g_postmeaslg_ul.append("")
        try:
            postmeas5g_postmeaslg_rsrp.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_rsrp"))["postmeaslg_rsrp__avg"],1))
        except:
            postmeas5g_postmeaslg_rsrp.append("")
        try:
            postmeas5g_postmeaslg_lte.append(round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_lte"))["postmeaslg_lte__avg"],1))
        except:
            postmeas5g_postmeaslg_lte.append("")
        data_testdl5g = [round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_dl"))["postmeaskt_dl__avg"],1)
                     ,round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_dl"))["postmeasskt_dl__avg"],1)
                     ,round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_dl"))["postmeaslg_dl__avg"],1)]
        df_testdl5g = pd.DataFrame(data_testdl5g)
        df_testdl5g = df_testdl5g.rank(axis=0, method='min', ascending=False)
        postmeas5grankdllist.append(str(round(df_testdl5g.iloc[0,0]))+"위")
        data_testul5g = [round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_ul"))["postmeaskt_ul__avg"],1)
                     ,round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_ul"))["postmeasskt_ul__avg"],1)
                     ,round(PostMeasure5G.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_ul"))["postmeaslg_ul__avg"],1)]
        df_testul5g = pd.DataFrame(data_testul5g)
        df_testul5g = df_testul5g.rank(axis=0, method='min', ascending=False)
        postmeas5grankullist.append(str(round(df_testul5g.iloc[0,0]))+"위")
    


    #사후측정 LTE
    postmeasltelist = [] 
    postmeaslterankdllist = []
    postmeaslterankullist = []
    postmeaslte_district = []
    postmeaslte_lastkt_dl = []
    postmeaslte_lastskt_dl = []
    postmeaslte_lastlg_dl = []
    postmeaslte_measkt_dl = []
    postmeaslte_measkt_ul = []
    postmeaslte_measkt_rsrp = []
    postmeaslte_measkt_sinr = []
    postmeaslte_postmeaskt_dl = []
    postmeaslte_postmeaskt_ul = []
    postmeaslte_postmeaskt_rsrp = []
    postmeaslte_postmeaskt_sinr = []
    postmeaslte_postmeasskt_dl = []
    postmeaslte_postmeasskt_ul = []
    postmeaslte_postmeasskt_rsrp = []
    postmeaslte_postmeasskt_sinr = []
    postmeaslte_postmeaslg_dl = []
    postmeaslte_postmeaslg_ul = []
    postmeaslte_postmeaslg_rsrp = []
    postmeaslte_postmeaslg_sinr = []
    postmeasltetotal_district = PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).count()
    try:
        postmeasltetotal_lastkt_dl = round(MeasLastyeardistrict.objects.get(district = '종합', nettype = 'LTE').KTDL)
    except:
        postmeasltetotal_lastkt_dl = ""
    try:
        postmeasltetotal_lastskt_dl = round(MeasLastyeardistrict.objects.get(district = '종합', nettype = 'LTE').SKTDL)
    except:
        postmeasltetotal_lastskt_dl = ""
    try:
        postmeasltetotal_lastlg_dl = round(MeasLastyeardistrict.objects.get(district = '종합', nettype = 'LTE').LGDL)
    except:
        postmeasltetotal_lastlg_dl = ""
    try:
        postmeasltetotal_measkt_dl = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("measkt_dl"))["measkt_dl__avg"],1)
    except:
        postmeasltetotal_measkt_dl = ""
    try:
        postmeasltetotal_measkt_ul = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("measkt_ul"))["measkt_ul__avg"],1)
    except:
        postmeasltetotal_measkt_ul = ""
    try:
        postmeasltetotal_measkt_rsrp = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("measkt_rsrp"))["measkt_rsrp__avg"],1)
    except:
        postmeasltetotal_measkt_rsrp = ""
    try:
        postmeasltetotal_measkt_sinr = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("measkt_sinr"))["measkt_sinr__avg"],1)
    except:
        postmeasltetotal_measkt_sinr = ""
    try:
        postmeasltetotal_postmeaskt_dl = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_dl"))["postmeaskt_dl__avg"],1)
    except:
        postmeasltetotal_postmeaskt_dl = ""
    try:
        postmeasltetotal_postmeaskt_ul = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_ul"))["postmeaskt_ul__avg"],1)
    except:
        postmeasltetotal_postmeaskt_ul = ""
    try:
        postmeasltetotal_postmeaskt_rsrp = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_rsrp"))["postmeaskt_rsrp__avg"],1)
    except:
        postmeasltetotal_postmeaskt_rsrp = ""
    try:
        postmeasltetotal_postmeaskt_sinr = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_sinr"))["postmeaskt_sinr__avg"],1)
    except:
        postmeasltetotal_postmeaskt_sinr = ""
    try:
        postmeasltetotal_postmeasskt_dl = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_dl"))["postmeasskt_dl__avg"],1)
    except:
        postmeasltetotal_postmeasskt_dl = ""
    try:
        postmeasltetotal_postmeasskt_ul = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_ul"))["postmeasskt_ul__avg"],1)
    except:
        postmeasltetotal_postmeasskt_ul = ""
    try:
        postmeasltetotal_postmeasskt_rsrp = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_rsrp"))["postmeasskt_rsrp__avg"],1)
    except:
        postmeasltetotal_postmeasskt_rsrp = ""
    try:
        postmeasltetotal_postmeasskt_sinr = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_sinr"))["postmeasskt_sinr__avg"],1)
    except:
        postmeasltetotal_postmeasskt_sinr = ""
    try:
        postmeasltetotal_postmeaslg_dl = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_dl"))["postmeaslg_dl__avg"],1)
    except:
        postmeasltetotal_postmeaslg_dl = ""
    try:
        postmeasltetotal_postmeaslg_ul = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_ul"))["postmeaslg_ul__avg"],1)
    except:
        postmeasltetotal_postmeaslg_ul = ""
    try:
        postmeasltetotal_postmeaslg_rsrp = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_rsrp"))["postmeaslg_rsrp__avg"],1)
    except:
        postmeasltetotal_postmeaslg_rsrp = ""
    try:
        postmeasltetotal_postmeaslg_sinr = round(PostMeasureLTE.objects.filter(measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_sinr"))["postmeaslg_sinr__avg"],1)
    except:
        postmeasltetotal_postmeaslg_sinr = ""
    for i in district_list:
        if PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).count() > 0 :
            postmeasltelist.append(i)
    for i in postmeasltelist:
        
        postmeaslte_district.append((PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate])).count())
        
        try:
            postmeaslte_lastkt_dl.append(round(MeasLastyeardistrict.objects.get(district = i, nettype = 'LTE').KTDL))
        except:
            postmeaslte_lastkt_dl.append("")
        try:
            postmeaslte_lastskt_dl.append(round(MeasLastyeardistrict.objects.get(district = i,nettype = 'LTE').SKTDL))
        except:
            postmeaslte_lastskt_dl.append("")
        try:
            postmeaslte_lastlg_dl.append(round(MeasLastyeardistrict.objects.get(district = i,nettype = 'LTE').LGDL))
        except:
            postmeaslte_lastlg_dl.append("")
        try:
            postmeaslte_measkt_dl.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("measkt_dl"))["measkt_dl__avg"],1))
        except:
            postmeaslte_measkt_dl.append("")
        try:
            postmeaslte_measkt_ul.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("measkt_ul"))["measkt_ul__avg"],1))
        except:
            postmeaslte_measkt_ul.append("")
        try:
            postmeaslte_measkt_rsrp.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("measkt_rsrp"))["measkt_rsrp__avg"],1))
        except:
            postmeaslte_measkt_rsrp.append("")
        try:
            postmeaslte_measkt_sinr.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("measkt_sinr"))["measkt_sinr__avg"],1))
        except:
            postmeaslte_measkt_sinr.append("")
        try:
            postmeaslte_postmeaskt_dl.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_dl"))["postmeaskt_dl__avg"],1))
        except:
            postmeaslte_postmeaskt_dl.append("")
        try:
            postmeaslte_postmeaskt_ul.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_ul"))["postmeaskt_ul__avg"],1))
        except:
            postmeaslte_postmeaskt_ul.append("")
        try:
            postmeaslte_postmeaskt_rsrp.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_rsrp"))["postmeaskt_rsrp__avg"],1))
        except:
            postmeaslte_postmeaskt_rsrp.append("")
        try:
            postmeaslte_postmeaskt_sinr.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_sinr"))["postmeaskt_sinr__avg"],1))
        except:
            postmeaslte_postmeaskt_sinr.append("")
        try:
            postmeaslte_postmeasskt_dl.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_dl"))["postmeasskt_dl__avg"],1))
        except:
            postmeaslte_postmeasskt_dl.append("")
        try:
            postmeaslte_postmeasskt_ul.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_ul"))["postmeasskt_ul__avg"],1))
        except:
            postmeaslte_postmeasskt_ul.append("")
        try:
            postmeaslte_postmeasskt_rsrp.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_rsrp"))["postmeasskt_rsrp__avg"],1))
        except:
            postmeaslte_postmeasskt_rsrp.append("")
        try:
            postmeaslte_postmeasskt_sinr.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_sinr"))["postmeasskt_sinr__avg"],1))
        except:
            postmeaslte_postmeasskt_sinr.append("")
        try:
            postmeaslte_postmeaslg_dl.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_dl"))["postmeaslg_dl__avg"],1))
        except:
            postmeaslte_postmeaslg_dl.append("")
        try:
            postmeaslte_postmeaslg_ul.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_ul"))["postmeaslg_ul__avg"],1))
        except:
            postmeaslte_postmeaslg_ul.append("")
        try:
            postmeaslte_postmeaslg_rsrp.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_rsrp"))["postmeaslg_rsrp__avg"],1))
        except:
            postmeaslte_postmeaslg_rsrp.append("")
        try:
            postmeaslte_postmeaslg_sinr.append(round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_sinr"))["postmeaslg_sinr__avg"],1))
        except:
            postmeaslte_postmeaslg_sinr.append("")
        data_testdllte = [round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_dl"))["postmeaskt_dl__avg"],1)
                     ,round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_dl"))["postmeasskt_dl__avg"],1)
                     ,round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_dl"))["postmeaslg_dl__avg"],1)]
        df_testdllte = pd.DataFrame(data_testdllte)
        df_testdllte = df_testdllte.rank(axis=0, method='min', ascending=True)
        postmeaslterankdllist.append(str(round(df_testdllte.iloc[0,0]))+"위")
        data_testullte = [round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaskt_ul"))["postmeaskt_ul__avg"],1)
                     ,round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeasskt_ul"))["postmeasskt_ul__avg"],1)
                     ,round(PostMeasureLTE.objects.filter(district = i,measdate__range=[firstday,hodate]).aggregate(Avg("postmeaslg_ul"))["postmeaslg_ul__avg"],1)]
        df_testullte = pd.DataFrame(data_testullte)
        df_testullte = df_testullte.rank(axis=0, method='min', ascending=False)
        postmeaslterankullist.append(str(round(df_testullte.iloc[0,0]))+"위")  
            
#측정대상
    regi = MeasPlan.objects.filter(planYear="2022")
#측정일자(처음~마지막) 
    firstdate = firstday
    lastdate = hodate
#리포트메세지    
    reportmsg = ReportMessage.objects.filter(measdate = hodate)
    
    # reportmsg_msg5G = ReportMessage.objects.get(measdate = hodate).msg5G
    # reportmsg_msgLTE = ReportMessage.objects.get(measdate = hodate).msgLTE
    # reportmsg_msgWiFi = ReportMessage.objects.get(measdate = hodate).msgWiFi
    # reportmsg_msgWeak = ReportMessage.objects.get(measdate = hodate).msgWeak
    # reportmsg_msg5Gafter = ReportMessage.objects.get(measdate = hodate).msg5Gafter
    # reportmsg_msgLTEafter = ReportMessage.objects.get(measdate = hodate).msgLTEafter
    
#측정전체    
    sregi = LastMeasDayClose.objects.filter(measdate__range=[firstday,hodate])
#당일측정
    tregi = LastMeasDayClose.objects.filter(measdate = hodate)
#5G측정전체개수    
    sregi5Ghjd = LastMeasDayClose.objects.filter(nettype = "5G NSA", mopho = "행정동",measdate__range=[firstday,hodate]).count()
    sregi5Gdagyo = LastMeasDayClose.objects.filter(Q(nettype = "5G NSA")&(Q(mopho = "다중이용시설")|Q(mopho = "교통인프라"))&Q(measdate__range=[firstday,hodate])).count()
    sregi5Gnsatotal = LastMeasDayClose.objects.filter(nettype = "5G NSA",measdate__range=[firstday,hodate]).count()
    sregi5Gsatotal = LastMeasDayClose.objects.filter(nettype = "5G SA",measdate__range=[firstday,hodate]).count()
    sregi5Gpublic = LastMeasDayClose.objects.filter(nettype = "5G 공동망",measdate__range=[firstday,hodate]).count()
    sregi5Gcv = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망")) & Q(mopho = "커버리지")&Q(measdate__range=[firstday,hodate])).count()
    sregi5Gtotal = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(measdate__range=[firstday,hodate])).count()
#5G당일측정전체개수   
    tregi5Ghjd = LastMeasDayClose.objects.filter(nettype = "5G NSA", mopho = "행정동", measdate = hodate).count()
    tregi5Gdagyo = LastMeasDayClose.objects.filter(Q(nettype = "5G NSA")&(Q(mopho = "다중이용시설")|Q(mopho = "교통인프라"))&Q(measdate = hodate)).count()
    tregi5Gnsatotal = LastMeasDayClose.objects.filter(nettype = "5G NSA",measdate = hodate).count()
    tregi5Gsatotal = LastMeasDayClose.objects.filter(nettype = "5G SA ",measdate = hodate).count()
    tregi5Gpublic = LastMeasDayClose.objects.filter(nettype = "5G 공동망",measdate = hodate).count()
    tregi5Gcv = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망")) & Q(mopho = "커버리지")&Q(measdate = hodate)).count()
    tregi5Gtotal = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(measdate = hodate)).count()
#5G지역별측정개수
    district5gcount = []
    for i in district_list:
        district5gcount.append(LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(district = i)&Q(measdate__range=[firstday,hodate])).count())
    city5gcount = []
    for i in city_list:
        city5gcount.append(LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(detailadd = i)&Q(measdate__range=[firstday,hodate])).count())
    facility5gcount = []
    for i in facility5g_list:
        facility5gcount.append(LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(detailadd = i)&Q(measdate__range=[firstday,hodate])).count())
    traffic5gcount = []
    for i in traffic5g_list:
        traffic5gcount.append(LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(detailadd = i)&Q(measdate__range=[firstday,hodate])).count())
    districtsa5gcount = []
    for i in district_list:
        districtsa5gcount.append(LastMeasDayClose.objects.filter(nettype = "5G SA", district = i,measdate__range=[firstday,hodate]).count())
    
#LTE측정전체개수
    sregiLTEbct = LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "대도시",measdate__range=[firstday,hodate]).count()
    sregiLTEmct = LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "중소도시",measdate__range=[firstday,hodate]).count()
    sregiLTEsct = LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "농어촌",measdate__range=[firstday,hodate]).count()
    sregiLTEib = LastMeasDayClose.objects.filter(nettype = "LTE", mopho = "인빌딩",measdate__range=[firstday,hodate]).count()
    sregiLTEtm = LastMeasDayClose.objects.filter(nettype = "LTE", mopho = "테마",measdate__range=[firstday,hodate]).count()
    sregiLTEcv = LastMeasDayClose.objects.filter(nettype = "LTE", mopho = "커버리지",measdate__range=[firstday,hodate]).count()
    sregiLTEtotal = LastMeasDayClose.objects.filter(nettype = "LTE",measdate__range=[firstday,hodate]).count()
#LTE당일측정전체개수    
    tregiLTEbct = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = hodate, detailadd = "대도시").count()
    tregiLTEmct = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = hodate, detailadd = "중소도시").count()
    tregiLTEsct = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = hodate, detailadd = "농어촌").count()
    tregiLTEib = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = hodate, mopho = "인빌딩").count()
    tregiLTEtm = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = hodate, mopho = "테마").count()
    tregiLTEcv = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = hodate, mopho = "커버리지").count()
    tregiLTEtotal = LastMeasDayClose.objects.filter(nettype = "LTE",  measdate = hodate).count()
#LTE지역별측정개수
    districtltecount = []
    for i in district_list:
        districtltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", district = i,measdate__range=[firstday,hodate]).count())
    bctltecount = []
    for i in district_list:
        bctltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "대도시" ,district = i,measdate__range=[firstday,hodate]).count())
    mctltecount = []
    for i in district_list:
        mctltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "중소도시" ,district = i,measdate__range=[firstday,hodate]).count())
    sctltecount = []
    for i in district_list:
        sctltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd = "농어촌" ,district = i,measdate__range=[firstday,hodate]).count())
    ibltecount = []
    for i in inbuildinglte_list:
        ibltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", mopho = "인빌딩" ,detailadd = i,measdate__range=[firstday,hodate]).count())
    tmltecount = []
    for i in themelte_list:
        tmltecount.append(LastMeasDayClose.objects.filter(nettype = "LTE", mopho = "테마" ,detailadd = i,measdate__range=[firstday,hodate]).count()) 

#WiFi측정전체개수
    sregiWiFisy = LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "상용",measdate__range=[firstday,hodate]).count()
    sregiWiFigb = LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "개방",measdate__range=[firstday,hodate]).count()
    sregiWiFipublic = LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "공공",measdate__range=[firstday,hodate]).count()
    sregiWiFitotal = LastMeasDayClose.objects.filter(nettype = "WiFi",measdate__range=[firstday,hodate]).count()
#WiFi당일측정전체개수
    tregiWiFisy = LastMeasDayClose.objects.filter(nettype = "WiFi",  measdate = hodate, mopho = "상용").count()
    tregiWiFigb = LastMeasDayClose.objects.filter(nettype = "WiFi",  measdate = hodate, mopho = "개방").count()
    tregiWiFipublic = LastMeasDayClose.objects.filter(nettype = "WiFi",  measdate = hodate, mopho = "공공").count()
    tregiWiFitotal = LastMeasDayClose.objects.filter(nettype = "WiFi",  measdate = hodate).count()
#WiFi지역별측정개수     
    districtWiFicount = []
    for i in district_list:
        districtWiFicount.append(LastMeasDayClose.objects.filter(nettype = "WiFi", district = i,measdate__range=[firstday,hodate]).count())
    sywificount = []
    for i in district_list:
        sywificount.append(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "상용" ,district = i,measdate__range=[firstday,hodate]).count())
    gbwificount = []
    for i in district_list:
        gbwificount.append(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "개방" ,district = i,measdate__range=[firstday,hodate]).count())
    publicwificount = []
    for i in district_list:
        publicwificount.append(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "공공" ,district = i,measdate__range=[firstday,hodate]).count())
    
#품질취약지역측정전체개수
    sregiweakdsr = LastMeasDayClose.objects.filter(mopho = "품질취약지역", detailadd = "등산로",measdate__range=[firstday,hodate]).count()
    sregiweakyghr = LastMeasDayClose.objects.filter(mopho = "품질취약지역", detailadd = "여객항로",measdate__range=[firstday,hodate]).count()
    sregiweakyids = LastMeasDayClose.objects.filter(mopho = "품질취약지역", detailadd = "유인도서",measdate__range=[firstday,hodate]).count()
    sregiweakhadr = LastMeasDayClose.objects.filter(mopho = "품질취약지역", detailadd = "해안도로",measdate__range=[firstday,hodate]).count()
    sregiweaktotal = LastMeasDayClose.objects.filter(mopho = "품질취약지역").count()
#품질취약지역당일측정전체개수   
    tregiweakdsr = LastMeasDayClose.objects.filter(mopho = "품질취약지역",  measdate = hodate, detailadd = "등산로").count()
    tregiweakyghr = LastMeasDayClose.objects.filter(mopho = "품질취약지역",  measdate = hodate, detailadd = "여객항로").count()
    tregiweakyids = LastMeasDayClose.objects.filter(mopho = "품질취약지역",  measdate = hodate, detailadd = "유인도서").count()
    tregiweakhadr = LastMeasDayClose.objects.filter(mopho = "품질취약지역",  measdate = hodate, detailadd = "해안도로").count()
    tregiweaktotal = LastMeasDayClose.objects.filter(mopho = "품질취약지역",  measdate = hodate).count()
#품질취약지역지역별측정개수    
    districtWeakcount = []
    for i in district_list:
        districtWeakcount.append(LastMeasDayClose.objects.filter(nettype = "품질취약지역", district = i,measdate__range=[firstday,hodate]).count())
    dsrweakcount = []
    for i in district_list:
        dsrweakcount.append(LastMeasDayClose.objects.filter(nettype = "품질취약지역", detailadd = "등산로" ,district = i,measdate__range=[firstday,hodate]).count())
    yghrweakcount = []
    for i in district_list:
        yghrweakcount.append(LastMeasDayClose.objects.filter(nettype = "품질취약지역", detailadd = "여객항로" ,district = i,measdate__range=[firstday,hodate]).count())
    yidsweakcount = []
    for i in district_list:
        yidsweakcount.append(LastMeasDayClose.objects.filter(nettype = "품질취약지역", detailadd = "유인도서" ,district = i,measdate__range=[firstday,hodate]).count())
    hadrweakcount = []
    for i in district_list:
        hadrweakcount.append(LastMeasDayClose.objects.filter(nettype = "품질취약지역", detailadd = "해안도로" ,district = i,measdate__range=[firstday,hodate]).count())
    
#모폴로지별작년측정결과
    #5G
    last5gbct = MeasLastyear5G.objects.filter(measarea='대도시')
    last5gmct = MeasLastyear5G.objects.filter(measarea='중소도시')
    last5ghjd = MeasLastyear5G.objects.filter(measarea='행정동')
    last5gdj = MeasLastyear5G.objects.filter(measarea='다중이용시설')
    last5gapt = MeasLastyear5G.objects.filter(measarea='아파트')
    last5gtraffic = MeasLastyear5G.objects.filter(measarea='교통인프라')
    last5gtotal = MeasLastyear5G.objects.filter(measarea='종합')
    #LTE
    lastltebct = MeasLastyearLTE.objects.filter(measarea='대도시')
    lastltemct = MeasLastyearLTE.objects.filter(measarea='중소도시')
    lastltesct = MeasLastyearLTE.objects.filter(measarea='농어촌')
    lastltehjd = MeasLastyearLTE.objects.filter(measarea='행정동')
    lastlteib = MeasLastyearLTE.objects.filter(measarea='인빌딩')
    lastltetm = MeasLastyearLTE.objects.filter(measarea='테마')
    lastltetotal = MeasLastyearLTE.objects.filter(measarea='종합')
    #WiFi
    lastwifigb = MeasLastyearWiFi.objects.filter(WiFitype='개방')
    lastwifisy = MeasLastyearWiFi.objects.filter(WiFitype='상용')
    lastwifipublic = MeasLastyearWiFi.objects.filter(WiFitype='공공')
    lastwifitotal = MeasLastyearWiFi.objects.filter(WiFitype='종합')
    
#5G측정결과
    result5g_list = [["downloadBandwidth","downloadBandwidth__avg"],["uploadBandwidth","uploadBandwidth__avg"],["dl_nr_percent","dl_nr_percent__avg"],["ul_nr_percent","ul_nr_percent__avg"],["udpJitter","udpJitter__avg"]] 
    bctnsa5g = []
    mctnsa5g = []
    hjdnsa5g = []
    djnsa5g = []
    aptnsa5g = []
    univnsa5g = []
    trafficnsa5g = []
    totalnsa5g = []
    for i in result5g_list :
        try:
            bctnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",detailadd = "대도시",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            bctnsa5g.append("")
        try:
            mctnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",detailadd = "중소도시",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            mctnsa5g.append("")
        try:
            hjdnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",mopho = "행정동",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            hjdnsa5g.append("")
        try:
            djnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",detailadd = "다중이용시설",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            djnsa5g.append("")
        try:
            aptnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",detailadd = "아파트",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            aptnsa5g.append("")
        try:
            univnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",detailadd = "대학교",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            univnsa5g.append("")
        try:
            trafficnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",mopho = "교통인프라",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            trafficnsa5g.append("")
        try:
            totalnsa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G NSA",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            totalnsa5g.append("")
         
#5G SA 측정결과 및 보고양식
    result5g_list = [["downloadBandwidth","downloadBandwidth__avg"],["uploadBandwidth","uploadBandwidth__avg"],["dl_nr_percent","dl_nr_percent__avg"],["ul_nr_percent","ul_nr_percent__avg"],["udpJitter","udpJitter__avg"]] 
    same_userinfo1 = [] 
    for n in range(len(LastMeasDayClose.objects.filter(nettype = "5G SA",measdate__range=[firstday,hodate]))):
        same_userinfo1.append(LastMeasDayClose.objects.filter(nettype = "5G SA",measdate__range=[firstday,hodate])[n].userInfo1)
    
    
    nsa5G_list = []
    sa5g=[]  
    nsa5g=[]      
    nsa5g_dl = 0
    nsa5g_ul = 0
    nsa5g_ltedl = 0
    nsa5g_lteul = 0
    nsa5g_delay = 0
    # for i in same_userinfo1:
    #         try:
    #             nsa5G_list.append(LastMeasDayClose.objects.filter(nettype = "5G NSA", userInfo1 = i))
    #         except:
    #             nsa5G_list.append("")
                      
    for i in result5g_list :
        try:
            sa5g.append(round(LastMeasDayClose.objects.filter(nettype = "5G SA",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
            
        except:
            sa5g.append("") 

    for n in same_userinfo1:
        try:
            
            nsa5g_dl += LastMeasDayClose.objects.get(nettype = "5G NSA" , userInfo1 = n,measdate__range=[firstday,hodate]).downloadBandwidth
            nsa5g_ul += LastMeasDayClose.objects.get(nettype = "5G NSA" , userInfo1 = n,measdate__range=[firstday,hodate]).uploadBandwidth
            nsa5g_ltedl += LastMeasDayClose.objects.get(nettype = "5G NSA" , userInfo1 = n,measdate__range=[firstday,hodate]).dl_nr_percent
            nsa5g_lteul += LastMeasDayClose.objects.get(nettype = "5G NSA" , userInfo1 = n,measdate__range=[firstday,hodate]).ul_nr_percent
            nsa5g_delay += LastMeasDayClose.objects.get(nettype = "5G NSA" , userInfo1 = n,measdate__range=[firstday,hodate]).udpJitter
            
            
            #nsa5g.append(round(nsa5G_list.objects.all().aggregate(Avg(i[0]))[i[1]],1))
        except:
            nsa5g_dl += 0
            nsa5g_ul += 0
            nsa5g_ltedl += 0
            nsa5g_lteul += 0
            nsa5g_delay += 0
    
    try:
        nsa5g.append(round(nsa5g_dl/len(same_userinfo1),1))
    except:
        nsa5g.append("")
    try:
        nsa5g.append(round(nsa5g_ul/len(same_userinfo1),1))
    except:
        nsa5g.append("")
    try:
        nsa5g.append(round(nsa5g_ltedl/len(same_userinfo1),1))
    except:
        nsa5g.append("")
    try:
        nsa5g.append(round(nsa5g_lteul/len(same_userinfo1),1))
    except:
        nsa5g.append("")
    try:
        nsa5g.append(round(nsa5g_delay/len(same_userinfo1),1))
    except:
        nsa5g.append("")   
    
    
    
    nsa5g_dl = 0
    nsa5g_ul = 0
    nsa5g_ltedl = 0
    nsa5g_lteul = 0
    nsa5g_delay = 0
    
#LTE측정결과
    resultlte_list = [["downloadBandwidth","downloadBandwidth__avg"],["uploadBandwidth","uploadBandwidth__avg"],["udpJitter","udpJitter__avg"]] 
    bctlte = []
    mctlte = []
    sctlte = []
    hjdlte = []
    iblte = []
    tmlte = []
    totallte = []
    for i in resultlte_list :                    
        try:
            bctlte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd="대도시",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            bctlte.append("")
        try:
            mctlte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd="중소도시",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            mctlte.append("")
        try:
            sctlte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", detailadd="농어촌",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            sctlte.append("")
        try:
            hjdlte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", mopho="행정동",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            hjdlte.append("")
        try:
            iblte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", mopho="인빌딩",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            iblte.append("")
        try:
            tmlte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE", mopho="테마",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            tmlte.append("")
        try:
            totallte.append(round(LastMeasDayClose.objects.filter(nettype = "LTE",measdate__range=[firstday,hodate]).aggregate(Avg(i[0]))[i[1]],1))
        except:
            totallte.append("")
                    
#품질취약지역측정결과
       
#wifi측정결과(종합)
    try:
        totalwifidl = round(LastMeasDayClose.objects.filter(nettype = "WiFi",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalwifidl = ""
    try:
        totalsywifidl = round(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "상용",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalsywifidl = ""
    try:
        totalgbwifidl = round(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "개방",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1)
    except:
        totalgbwifidl = ""
    try:
        totalwifiul = round(LastMeasDayClose.objects.filter(nettype = "WiFi",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalwifiul = ""
    try:
        totalsywifiul = round(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "상용",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalsywifiul = ""
    try:
        totalgbwifiul = round(LastMeasDayClose.objects.filter(nettype = "WiFi", mopho = "개방",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1)
    except:
        totalgbwifiul = ""

#wifi측정결과(센터별)
    wificenterdl = []
    wificenterul = []
    wificenterdl2 = []
    wificenterul2 = []
    for i in center_list1:
        try:
            wificenterdl.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="상용",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
        except:
            wificenterdl.append("")
        try:
            wificenterdl.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="개방",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
        except:
            wificenterdl.append("")
        try:    
            wificenterul.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="상용",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
        except:    
            wificenterul.append("")
        try:    
            wificenterul.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="개방",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
        except:    
            wificenterul.append("")
    for i in center_list2:
        try:
            wificenterdl2.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="상용",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
        except:
            wificenterdl2.append("")
        try:
            wificenterdl2.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="개방",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
        except:
            wificenterdl2.append("")
        try:    
            wificenterul2.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="상용",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
        except:    
            wificenterul2.append("")
        try:    
            wificenterul2.append(round(LastMeasDayClose.objects.filter(nettype = "WiFi", center=i, mopho="개방",measdate__range=[firstday,hodate]).exclude(detailadd = '지하철').aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
        except:    
            wificenterul2.append("")

#wifi 측정결과(지역별)
    
    train_list = ['부산','대구','광주','대전']
    lasttrain_list = ['종합','수도권','부산','대구','광주','대전']
    wifitraindl = []
    wifitrainul = []
    wifitrainlastdl = []
    wifitrainlastul = []
    for i in lasttrain_list:
        try:
            wifitrainlastdl.append(round( MeasLastyeardistrict.objects.get(nettype = "WiFi지하철", district=i).KTDL))
        except:
            wifitrainlastdl.append("")
        try:
            wifitrainlastul.append(round( MeasLastyeardistrict.objects.get(nettype = "WiFi지하철", district=i).KTUL))
        except:
            wifitrainlastul.append("")
    try:
        wifitraindl.append(round(LastMeasDayClose.objects.filter(Q(nettype = "WiFi")&(Q(district='서울')|Q(district='인천')|Q(district='경기')|
                                                                                  Q(district='부산')|Q(district='대구')|Q(district='광주')|
                                                                                  Q(district='대전'))&Q(detailadd='지하철')&Q(measdate__range=[firstday,hodate])).aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
    except:
        wifitraindl.append("")
    try:
        wifitraindl.append(round(LastMeasDayClose.objects.filter(Q(nettype = "WiFi")&(Q(district='서울')|Q(district='인천')|Q(district='경기'))
                                                             &Q(detailadd='지하철')&Q(measdate__range=[firstday,hodate])).aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
    except:
        wifitraindl.append("")
    try:
        wifitrainul.append(round(LastMeasDayClose.objects.filter(Q(nettype = "WiFi")&(Q(district='서울')|Q(district='인천')|Q(district='경기')|
                                                                                  Q(district='부산')|Q(district='대구')|Q(district='광주')|
                                                                                  Q(district='대전'))&Q(detailadd='지하철')&Q(measdate__range=[firstday,hodate])).aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
    except:
        wifitrainul.append("")
    try:
        wifitrainul.append(round(LastMeasDayClose.objects.filter(Q(nettype = "WiFi")&(Q(district='서울')|Q(district='인천')|Q(district='경기'))
                                                             &Q(detailadd='지하철')&Q(measdate__range=[firstday,hodate])).aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
    except:
        wifitrainul.append("")
    for i in train_list:
        try:
            wifitraindl.append(round(LastMeasDayClose.objects.filter(Q(nettype = "WiFi")&Q(district=i)&Q(detailadd='지하철')&Q(measdate__range=[firstday,hodate])).aggregate(Avg("downloadBandwidth"))["downloadBandwidth__avg"],1))
        except:
            wifitraindl.append("")
        try:
            wifitrainul.append(round(LastMeasDayClose.objects.filter(Q(nettype = "WiFi")&Q(district=i)&Q(detailadd='지하철')&Q(measdate__range=[firstday,hodate])).aggregate(Avg("uploadBandwidth"))["uploadBandwidth__avg"],1))
        except:
            wifitrainul.append("")

#금일 측정 결과 
    tresult5g = LastMeasDayClose.objects.filter((Q(nettype = "5G NSA")|Q(nettype = "5G SA")|Q(nettype = "5G 공동망"))&Q(measdate = hodate))
    tresultlte = LastMeasDayClose.objects.filter(nettype = "LTE", measdate = hodate)
    tresultwifi = LastMeasDayClose.objects.filter(nettype = "WiFi", measdate = hodate)
    tresultweak = LastMeasDayClose.objects.filter(nettype = "품질취약지역", measdate = hodate)

#리포트 날짜 스트링변환
    report_day = hodate.strftime('%Y%m%d') 
    report_firstday = firstdate.strftime('%Y%m%d') 
    
   
    context = { 
    'reportdate':reportdate,'hodate':hodate,'report_day':report_day,'report_firstday':report_firstday,
    'wificenterdl':wificenterdl,'wificenterul':wificenterul,'center_list1':center_list1,'center_list2':center_list2,'district_list':district_list,
    'wificenterdl2':wificenterdl2,'wificenterul2':wificenterul2,
    'district5gcount':district5gcount,'city5gcount':city5gcount,'facility5gcount':facility5gcount,'traffic5gcount':traffic5gcount,'districtsa5gcount':districtsa5gcount,
    'districtltecount':districtltecount,'bctltecount':bctltecount,'mctltecount':mctltecount,'sctltecount':sctltecount,'ibltecount':ibltecount,'tmltecount':tmltecount,
    'districtWiFicount':districtWiFicount,'sywificount':sywificount,'gbwificount':gbwificount,'publicwificount':publicwificount,
    'districtWeakcount':districtWeakcount,'dsrweakcount':dsrweakcount,'yghrweakcount':yghrweakcount,'yidsweakcount':yidsweakcount,'hadrweakcount':hadrweakcount,
    'tresult5g':tresult5g,'tresultlte':tresultlte,'tresultwifi':tresultwifi,'tresultweak':tresultweak,
    # 'reportmsg_msg5G':reportmsg_msg5G,
    # 'reportmsg_msgLTE':reportmsg_msgLTE,
    # 'reportmsg_msgWiFi':reportmsg_msgWiFi,
    # 'reportmsg_msgWeak':reportmsg_msgWeak,
    # 'reportmsg_msg5Gafter':reportmsg_msg5Gafter,
    # 'reportmsg_msgLTEafter':reportmsg_msgLTEafter,
    'regi':regi, 'reportmsg':reportmsg,'sregi':sregi,'firstdate':firstdate,'lastdate':lastdate,
    'tregi5Ghjd':tregi5Ghjd,'tregi5Gdagyo':tregi5Gdagyo,'tregi5Gnsatotal':tregi5Gnsatotal,'tregi5Gsatotal':tregi5Gsatotal, 'tregi5Gpublic':tregi5Gpublic,'tregi5Gcv':tregi5Gcv,'tregi5Gtotal':tregi5Gtotal,
    'sregi5Ghjd':sregi5Ghjd,'sregi5Gdagyo':sregi5Gdagyo,'sregi5Gnsatotal':sregi5Gnsatotal,'sregi5Gsatotal':sregi5Gsatotal,'sregi5Gpublic':sregi5Gpublic,'sregi5Gcv':sregi5Gcv,'sregi5Gtotal':sregi5Gtotal,
    'sregiLTEbct':sregiLTEbct, 'sregiLTEmct':sregiLTEmct,'sregiLTEsct':sregiLTEsct, 'sregiLTEib':sregiLTEib,'sregiLTEtm':sregiLTEtm, 'sregiLTEcv':sregiLTEcv,'sregiLTEtotal':sregiLTEtotal, 
    'tregiLTEbct':tregiLTEbct,'tregiLTEmct':tregiLTEmct, 'tregiLTEsct':tregiLTEsct,'tregiLTEib':tregiLTEib, 'tregiLTEtm':tregiLTEtm,'tregiLTEcv':tregiLTEcv, 'tregiLTEtotal':tregiLTEtotal,
    'sregiWiFisy':sregiWiFisy,'sregiWiFigb':sregiWiFigb,'sregiWiFitotal':sregiWiFitotal,'tregiWiFisy':tregiWiFisy,'tregiWiFigb':tregiWiFigb,'tregiWiFitotal':tregiWiFitotal,'sregiweakdsr':sregiweakdsr,
    'sregiweakyghr':sregiweakyghr,'sregiweakyids':sregiweakyids,'sregiweakhadr':sregiweakhadr,'sregiweaktotal':sregiweaktotal,'tregiweakdsr':tregiweakdsr,'tregiweakyghr':tregiweakyghr,'tregiweakyids':tregiweakyids,'tregiweakhadr':tregiweakhadr,
    'tregiweaktotal':tregiweaktotal,
    'bctnsa5g':bctnsa5g,'mctnsa5g':mctnsa5g,'hjdnsa5g':hjdnsa5g,'djnsa5g':djnsa5g,'aptnsa5g':aptnsa5g,'univnsa5g':univnsa5g,'trafficnsa5g':trafficnsa5g,'totalnsa5g':totalnsa5g,'sa5g':sa5g,'nsa5g':nsa5g,
    'bctlte':bctlte,'mctlte':mctlte,'sctlte':sctlte,'hjdlte':hjdlte,'iblte':iblte,'tmlte':tmlte,'totallte':totallte,
    'last5gbct':last5gbct,'last5gmct':last5gmct,'last5ghjd':last5ghjd,'last5gdj':last5gdj,'last5gapt':last5gapt,'last5gtraffic':last5gtraffic,'last5gtotal':last5gtotal,
    'lastltebct':lastltebct,'lastltemct':lastltemct,'lastltesct':lastltesct,'lastltehjd':lastltehjd,'lastlteib':lastlteib,'lastltetm':lastltetm,'lastltetotal':lastltetotal,
    'lastwifigb':lastwifigb,'lastwifisy':lastwifisy,'lastwifipublic':lastwifipublic,'lastwifitotal':lastwifitotal,
    'wifitraindl':wifitraindl,'wifitrainul':wifitrainul,'wifitrainlastdl':wifitrainlastdl,'wifitrainlastul':wifitrainlastul,
    'totalwifidl':totalwifidl,'totalsywifidl':totalsywifidl,'totalgbwifidl':totalgbwifidl,'totalwifiul':totalwifiul,'totalsywifiul':totalsywifiul,'totalgbwifiul':totalgbwifiul,
    'postmeasure5g':postmeasure5g,'postmeasurelte':postmeasurelte,
    'postmeas5glist':postmeas5glist, 'postmeas5grankdllist':postmeas5grankdllist,'postmeas5grankullist':postmeas5grankullist,
    'postmeas5gtotal_district':postmeas5gtotal_district,'postmeas5gtotal_lastkt_dl':postmeas5gtotal_lastkt_dl,
    'postmeas5gtotal_lastskt_dl':postmeas5gtotal_lastskt_dl,'postmeas5gtotal_lastlg_dl':postmeas5gtotal_lastlg_dl,
    'postmeas5gtotal_measkt_dl':postmeas5gtotal_measkt_dl,
    'postmeas5gtotal_measkt_ul':postmeas5gtotal_measkt_ul,
    'postmeas5gtotal_measkt_rsrp':postmeas5gtotal_measkt_rsrp,
    'postmeas5gtotal_measkt_lte':postmeas5gtotal_measkt_lte,
    'postmeas5gtotal_postmeaskt_dl':postmeas5gtotal_postmeaskt_dl,
    'postmeas5gtotal_postmeaskt_ul':postmeas5gtotal_postmeaskt_ul,
    'postmeas5gtotal_postmeaskt_rsrp':postmeas5gtotal_postmeaskt_rsrp,
    'postmeas5gtotal_postmeaskt_lte':postmeas5gtotal_postmeaskt_lte,
    'postmeas5gtotal_postmeasskt_dl':postmeas5gtotal_postmeasskt_dl,
    'postmeas5gtotal_postmeasskt_ul':postmeas5gtotal_postmeasskt_ul,
    'postmeas5gtotal_postmeasskt_rsrp':postmeas5gtotal_postmeasskt_rsrp,
    'postmeas5gtotal_postmeasskt_lte':postmeas5gtotal_postmeasskt_lte,
    'postmeas5gtotal_postmeaslg_dl':postmeas5gtotal_postmeaslg_dl,
    'postmeas5gtotal_postmeaslg_ul':postmeas5gtotal_postmeaslg_ul,
    'postmeas5gtotal_postmeaslg_rsrp':postmeas5gtotal_postmeaslg_rsrp,
    'postmeas5gtotal_postmeaslg_lte':postmeas5gtotal_postmeaslg_lte,
    'postmeas5g_district':postmeas5g_district,'postmeas5g_lastkt_dl':postmeas5g_lastkt_dl,
    'postmeas5g_lastskt_dl':postmeas5g_lastskt_dl,'postmeas5g_lastlg_dl':postmeas5g_lastlg_dl,
    'postmeas5g_measkt_dl':postmeas5g_measkt_dl,
    'postmeas5g_measkt_ul':postmeas5g_measkt_ul,
    'postmeas5g_measkt_rsrp':postmeas5g_measkt_rsrp,
    'postmeas5g_measkt_lte':postmeas5g_measkt_lte,
    'postmeas5g_postmeaskt_dl':postmeas5g_postmeaskt_dl,
    'postmeas5g_postmeaskt_ul':postmeas5g_postmeaskt_ul,
    'postmeas5g_postmeaskt_rsrp':postmeas5g_postmeaskt_rsrp,
    'postmeas5g_postmeaskt_lte':postmeas5g_postmeaskt_lte,
    'postmeas5g_postmeasskt_dl':postmeas5g_postmeasskt_dl,
    'postmeas5g_postmeasskt_ul':postmeas5g_postmeasskt_ul,
    'postmeas5g_postmeasskt_rsrp':postmeas5g_postmeasskt_rsrp,
    'postmeas5g_postmeasskt_lte':postmeas5g_postmeasskt_lte,
    'postmeas5g_postmeaslg_dl':postmeas5g_postmeaslg_dl,
    'postmeas5g_postmeaslg_ul':postmeas5g_postmeaslg_ul,
    'postmeas5g_postmeaslg_rsrp':postmeas5g_postmeaslg_rsrp,
    'postmeas5g_postmeaslg_lte':postmeas5g_postmeaslg_lte,
    
    'postmeasltelist':postmeasltelist, 'postmeaslterankdllist':postmeaslterankdllist,'postmeaslterankullist':postmeaslterankullist,
    'postmeasltetotal_district':postmeasltetotal_district,'postmeasltetotal_lastkt_dl':postmeasltetotal_lastkt_dl,
    'postmeasltetotal_lastskt_dl':postmeasltetotal_lastskt_dl,'postmeasltetotal_lastlg_dl':postmeasltetotal_lastlg_dl,
    'postmeasltetotal_measkt_dl':postmeasltetotal_measkt_dl,
    'postmeasltetotal_measkt_ul':postmeasltetotal_measkt_ul,
    'postmeasltetotal_measkt_rsrp':postmeasltetotal_measkt_rsrp,
    'postmeasltetotal_measkt_sinr':postmeasltetotal_measkt_sinr,
    'postmeasltetotal_postmeaskt_dl':postmeasltetotal_postmeaskt_dl,
    'postmeasltetotal_postmeaskt_ul':postmeasltetotal_postmeaskt_ul,
    'postmeasltetotal_postmeaskt_rsrp':postmeasltetotal_postmeaskt_rsrp,
    'postmeasltetotal_postmeaskt_sinr':postmeasltetotal_postmeaskt_sinr,
    'postmeasltetotal_postmeasskt_dl':postmeasltetotal_postmeasskt_dl,
    'postmeasltetotal_postmeasskt_ul':postmeasltetotal_postmeasskt_ul,
    'postmeasltetotal_postmeasskt_rsrp':postmeasltetotal_postmeasskt_rsrp,
    'postmeasltetotal_postmeasskt_sinr':postmeasltetotal_postmeasskt_sinr,
    'postmeasltetotal_postmeaslg_dl':postmeasltetotal_postmeaslg_dl,
    'postmeasltetotal_postmeaslg_ul':postmeasltetotal_postmeaslg_ul,
    'postmeasltetotal_postmeaslg_rsrp':postmeasltetotal_postmeaslg_rsrp,
    'postmeasltetotal_postmeaslg_sinr':postmeasltetotal_postmeaslg_sinr,
    'postmeaslte_district':postmeaslte_district,'postmeaslte_lastkt_dl':postmeaslte_lastkt_dl,
    'postmeaslte_lastskt_dl':postmeaslte_lastskt_dl,'postmeaslte_lastlg_dl':postmeaslte_lastlg_dl,
    'postmeaslte_measkt_dl':postmeaslte_measkt_dl,
    'postmeaslte_measkt_ul':postmeaslte_measkt_ul,
    'postmeaslte_measkt_rsrp':postmeaslte_measkt_rsrp,
    'postmeaslte_measkt_sinr':postmeaslte_measkt_sinr,
    'postmeaslte_postmeaskt_dl':postmeaslte_postmeaskt_dl,
    'postmeaslte_postmeaskt_ul':postmeaslte_postmeaskt_ul,
    'postmeaslte_postmeaskt_rsrp':postmeaslte_postmeaskt_rsrp,
    'postmeaslte_postmeaskt_sinr':postmeaslte_postmeaskt_sinr,
    'postmeaslte_postmeasskt_dl':postmeaslte_postmeasskt_dl,
    'postmeaslte_postmeasskt_ul':postmeaslte_postmeasskt_ul,
    'postmeaslte_postmeasskt_rsrp':postmeaslte_postmeasskt_rsrp,
    'postmeaslte_postmeasskt_sinr':postmeaslte_postmeasskt_sinr,
    'postmeaslte_postmeaslg_dl':postmeaslte_postmeaslg_dl,
    'postmeaslte_postmeaslg_ul':postmeaslte_postmeaslg_ul,
    'postmeaslte_postmeaslg_rsrp':postmeaslte_postmeaslg_rsrp,
    'postmeaslte_postmeaslg_sinr':postmeaslte_postmeaslg_sinr,
    }

    return context

# -------------------------------------------------------------------------------------------------
# 대상등록 페이지 - 측정대상, 측정완료, 전년도결과, 추가기입사항
# [ 고민해야 하는 사항 ]
#  - JSON형태의 컨텍스트를 만드는 코드 정규화
# -------------------------------------------------------------------------------------------------
def get_measplan_cntx(request):
    """ 측정대상등록 페이지에 보여질 데이터를 조회해서 JSON으로 반환하는 함수
        - 파라미터:
          . year : 해당년도
        - 반환값: context (JSON형태)
    """
    measplan = MeasPlan.objects.all()
    
    yy_text = request.GET.get('planYear')
    yy_list = MeasPlan.objects.filter(planYear=yy_text)
    
    

    context = {'measplan':measplan, 
    'yy_text':yy_text,'yy_list':yy_list,
    }

    return context

# -------------------------------------------------------------------------------------------------
# 측정마감데이터 확인페이지
# 
#  
# -------------------------------------------------------------------------------------------------
def get_measclose_cntx(request):
    """ 측정대상등록 페이지에 보여질 데이터를 조회해서 JSON으로 반환하는 함수
        - 파라미터:
          . year : 해당년도
        - 반환값: context (JSON형태)
    """
    
    measclose = LastMeasDayClose.objects.all()
    
    

    context = {'measclose':measclose,'networkid_list':networkid_list,
               'district_list':district_list,'center_list':center_list,'city_list':city_list ,'facility5g_list':facility5g_list,'traffic5g_list':traffic5g_list,
    'inbuildinglte_list':inbuildinglte_list,'themelte_list':themelte_list,
    }

    return context


# -------------------------------------------------------------------------------------------------
# 측정완료 등록 및 수정
# -------------------------------------------------------------------------------------------------
def updage__measplan(request):
    """ 측정대상 계획을 저장하는 함수
        - 파라미터
          . request: HttpRequest
        - 반환값: 없음
    """
    measplan = MeasPlan() #빈 객체 생성
    measplan.planYear = request.POST['planYear']
    # measplan.hjd5G = request.POST['hjd5G']
    # measplan.dg5G = request.POST['dg5G']
    # measplan.cv5G = request.POST['cv5G']
    measplan.bctLTE = request.POST['bctLTE']
    measplan.mctLTE = request.POST['mctLTE']
    measplan.sctLTE = request.POST['sctLTE']
    measplan.ibLTE = request.POST['ibLTE']
    measplan.tmLTE = request.POST['tmLTE']
    measplan.cvLTE = request.POST['cvLTE']
    measplan.syWiFi = request.POST['syWiFi']
    measplan.gbWiFi = request.POST['gbWiFi']
    measplan.dsrWeak = request.POST['dsrWeak']
    measplan.yghrWeak = request.POST['yghrWeak']
    measplan.yidsWeak = request.POST['yidsWeak']
    measplan.hadrWeak = request.POST['hadrWeak']


    measplan.cv5G = request.POST['cv5G']
    measplan.cvjs5G = request.POST['cvjs5G']
    measplan.nsadg5G = request.POST['nsadg5G']
    measplan.nsahjd5G = request.POST['nsahjd5G']
    measplan.nsapublic5G = request.POST['nsapublic5G']
    measplan.sa5G = request.POST['sa5G']
    measplan.publicWiFi = request.POST['publicWiFi']
    
    measplan.totalnsa5G = int(measplan.nsadg5G)+ int(measplan.nsahjd5G)


    measplan.total5G = int(measplan.cv5G)+ int(measplan.cvjs5G)+ int(measplan.nsadg5G)+ int(measplan.nsahjd5G)+ int(measplan.nsapublic5G)+ int(measplan.sa5G)
    measplan.totalLTE = int(measplan.bctLTE)+ int(measplan.mctLTE)+ int(measplan.sctLTE)+ int(measplan.ibLTE)+ int(measplan.tmLTE)+ int(measplan.cvLTE)
    measplan.totalWiFi = int(measplan.syWiFi)+ int(measplan.gbWiFi)
    measplan.totalWeakArea = int(measplan.dsrWeak)+ int(measplan.yghrWeak)+ int(measplan.yidsWeak)+ int(measplan.hadrWeak)
    measplan.total = measplan.total5G + measplan.totalLTE + measplan.totalWiFi + measplan.totalWeakArea

    MeasPlan.objects.filter(planYear = measplan.planYear).delete()

    measplan.save()

    return


# -------------------------------------------------------------------------------------------------
# 전년도 결과 등록 및 수정(5G)
# -------------------------------------------------------------------------------------------------
def update_measlastyear5G(request):
    """ 전년도 결과 등록 및 수정하는 함수
        - 파라미터
          . request: HttpRequest
        - 반환값: 없음
    """
    # 빈 객체를 생성한다.
    measlastyear5G = MeasLastyear5G()
    measlastyear5G.bctDL = request.POST['bctDL']
    measlastyear5G.bctUL = request.POST['bctUL']
    measlastyear5G.bctLTE = request.POST['bctLTE']
    measlastyear5G.bctsucc = request.POST['bctsucc']
    measlastyear5G.bctdelay = request.POST['bctdelay']

    measlastyear5G.mctDL = request.POST['mctDL']
    measlastyear5G.mctUL = request.POST['mctUL']
    measlastyear5G.mctLTE = request.POST['mctLTE']
    measlastyear5G.mctsucc = request.POST['mctsucc']
    measlastyear5G.mctdelay = request.POST['mctdelay']

    measlastyear5G.totalctDL = request.POST['totalctDL']
    measlastyear5G.totalctUL = request.POST['totalctUL']
    measlastyear5G.totalctLTE = request.POST['totalctLTE']
    measlastyear5G.totalctsucc = request.POST['totalctsucc']
    measlastyear5G.totalctdelay = request.POST['totalctdelay']

    measlastyear5G.djDL = request.POST['djDL']
    measlastyear5G.djUL = request.POST['djUL']
    measlastyear5G.djLTE = request.POST['djLTE']
    measlastyear5G.djsucc = request.POST['djsucc']
    measlastyear5G.djdelay = request.POST['djdelay']

    measlastyear5G.aptDL = request.POST['aptDL']
    measlastyear5G.aptUL = request.POST['aptUL']
    measlastyear5G.aptLTE = request.POST['aptLTE']
    measlastyear5G.aptsucc = request.POST['aptsucc']
    measlastyear5G.aptdelay = request.POST['aptdelay']

    measlastyear5G.univDL = request.POST['univDL']
    measlastyear5G.univUL = request.POST['univUL']
    measlastyear5G.univLTE = request.POST['univLTE']
    measlastyear5G.univsucc = request.POST['univsucc']
    measlastyear5G.univdelay = request.POST['univdelay']

    measlastyear5G.trafficDL = request.POST['trafficDL']
    measlastyear5G.trafficUL = request.POST['trafficUL']
    measlastyear5G.trafficLTE = request.POST['trafficLTE']
    measlastyear5G.trafficsucc = request.POST['trafficsucc']
    measlastyear5G.trafficdelay = request.POST['trafficdelay']

    measlastyear5G.areatotalDL = round((float(measlastyear5G.bctDL)+float(measlastyear5G.mctDL)+float(measlastyear5G.djDL)+float(measlastyear5G.aptDL)+float(measlastyear5G.univDL)+float(measlastyear5G.trafficDL))/6,1)
    measlastyear5G.areatotalUL = round((float(measlastyear5G.bctUL)+float(measlastyear5G.mctUL)+float(measlastyear5G.djUL)+float(measlastyear5G.aptUL)+float(measlastyear5G.univUL)+float(measlastyear5G.trafficUL))/6,1)
    measlastyear5G.areatotalLTE = round((float(measlastyear5G.bctLTE)+float(measlastyear5G.mctLTE)+float(measlastyear5G.djLTE)+float(measlastyear5G.aptLTE)+float(measlastyear5G.univLTE)+float(measlastyear5G.trafficLTE))/6,1)
    measlastyear5G.areatotalsucc = round((float(measlastyear5G.bctsucc)+float(measlastyear5G.mctsucc)+float(measlastyear5G.djsucc)+float(measlastyear5G.aptsucc)+float(measlastyear5G.univsucc)+float(measlastyear5G.trafficsucc))/6,1)
    measlastyear5G.areatotaldelay = round((float(measlastyear5G.bctdelay)+float(measlastyear5G.mctdelay)+float(measlastyear5G.djdelay)+float(measlastyear5G.aptdelay)+float(measlastyear5G.univdelay)+float(measlastyear5G.trafficdelay))/6,1)

    MeasLastyear5G.objects.all().delete()

    measlastyear5G.save()

    return
        

# -------------------------------------------------------------------------------------------------
# 전년도 결과 등록 및 수정(LTE)
# -------------------------------------------------------------------------------------------------
def update_measlastyearLTE(request):

    measlastyearLTE = MeasLastyearLTE() #빈 객체 생성
    measlastyearLTE.bctDL = request.POST['bctDL']
    measlastyearLTE.bctUL = request.POST['bctUL']

    measlastyearLTE.bctsucc = request.POST['bctsucc']
    measlastyearLTE.bctdelay = request.POST['bctdelay']

    measlastyearLTE.mctDL = request.POST['mctDL']
    measlastyearLTE.mctUL = request.POST['mctUL']

    measlastyearLTE.mctsucc = request.POST['mctsucc']
    measlastyearLTE.mctdelay = request.POST['mctdelay']

    measlastyearLTE.sctDL = request.POST['sctDL']
    measlastyearLTE.sctUL = request.POST['sctUL']

    measlastyearLTE.sctsucc = request.POST['sctsucc']
    measlastyearLTE.sctdelay = request.POST['sctdelay']

    measlastyearLTE.totalctDL = request.POST['totalctDL']
    measlastyearLTE.totalctUL = request.POST['totalctUL']

    measlastyearLTE.totalctsucc = request.POST['totalctsucc']
    measlastyearLTE.totalctdelay = request.POST['totalctdelay']

    measlastyearLTE.ibDL = request.POST['ibDL']
    measlastyearLTE.ibUL = request.POST['ibUL']

    measlastyearLTE.ibsucc = request.POST['ibsucc']
    measlastyearLTE.ibdelay = request.POST['ibdelay']

    measlastyearLTE.tmDL = request.POST['tmDL']
    measlastyearLTE.tmUL = request.POST['tmUL']

    measlastyearLTE.tmsucc = request.POST['tmsucc']
    measlastyearLTE.tmdelay = request.POST['tmdelay']

    measlastyearLTE.areatotalDL = round((float(measlastyearLTE.bctDL)+float(measlastyearLTE.mctDL)+float(measlastyearLTE.sctDL)+float(measlastyearLTE.ibDL)+float(measlastyearLTE.tmDL))/5,1)
    measlastyearLTE.areatotalUL = round((float(measlastyearLTE.bctUL)+float(measlastyearLTE.mctUL)+float(measlastyearLTE.sctUL)+float(measlastyearLTE.ibUL)+float(measlastyearLTE.tmUL))/5,1)
    measlastyearLTE.areatotalsucc = round((float(measlastyearLTE.bctsucc)+float(measlastyearLTE.mctsucc)+float(measlastyearLTE.sctsucc)+float(measlastyearLTE.ibsucc)+float(measlastyearLTE.tmsucc))/5,1)
    measlastyearLTE.areatotaldelay = round((float(measlastyearLTE.bctdelay)+float(measlastyearLTE.mctdelay)+float(measlastyearLTE.sctdelay)+float(measlastyearLTE.ibdelay)+float(measlastyearLTE.tmdelay))/5,1)

    MeasLastyearLTE.objects.all().delete()

    measlastyearLTE.save()
        
    return
  

