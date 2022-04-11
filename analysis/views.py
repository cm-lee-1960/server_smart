# from django.shortcuts import render,redirect
# from django.contrib.auth.decorators import login_required
# from monitor.models import Phone
# from .models import MeasPlan, MeasResult,ReportMessage, MeasLastyear5G, MeasLastyearLTE
# import pandas as pd
# import datetime
# from django.db.models import Sum
# from makereport import *
# import sys

from multiprocessing.sharedctypes import Value
from operator import mod
from django.forms import CharField
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from monitor.models import Phone
from analysis.models import MeasPlan, MeasResult,ReportMessage, MeasLastyear5G, MeasLastyearLTE
import pandas as pd
import datetime
from django.db.models import Sum
from .makereport import *
from django.urls import reverse
from .forms import MeasLastyear5GForm, MeasLastyearLTEForm

from monitor.models import *
from management.models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpRequest, HttpResponse, HttpResponsePermanentRedirect
from .ajax import *

from django.views.generic import ListView
from django.shortcuts import get_list_or_404
from django.views.generic import TemplateView
from monitor.serializers import PhoneGroupSerializerOrder, MessageSerializer


###################################################################################################
# 분석 처리모듈
# -------------------------------------------------------------------------------------------------
# 2022-03-23 - 모듈 정리 및 주석 추가
# 2022-03-24 - 데이터 비동기 호출(Ajax) 함수 추가 -> ajax.py
# 2022-03-29 - 그룹 리스트 가져오는 함수 추가 -> get_list
# 2022-03-31 - 메세지 리스트 가져오는 함수 추가 -> get_list_m
###################################################################################################

# -------------------------------------------------------------------------------------------------
# 홈(Home) 페이지
# -------------------------------------------------------------------------------------------------
#FBV grouplist
#global start_flag  ## 처음임을 확인
#start_flag = 0

def get_listview(request):
    """함수기반 뷰 FBV 그룹데이터 호출 뷰"""
    #global start_flag
    data = {}
    if request.method== "POST":
        
        toDate = request.POST['date'].split('-')
        toDate_str = "".join(toDate)
        print("여기들어왓다")
        print(toDate_str)
        
            
        phonegroup = PhoneGroup.objects.filter(measdate=toDate_str, ispId='45008',manage=1).order_by('-active')
        ##print(phonegroup)
        fields = ['p_center','measuringTeam','userInfo1','p_morpol','networkId','dl_count','downloadBandwidth', 
                'ul_count','uploadBandwidth','nr_percent','event_count','active','last_updated_dt','id']
                  ## id는 메세지를 불러오기위하여
        #print(start_flag)

        if len(phonegroup) != 0:
            serializer = PhoneGroupSerializerOrder(phonegroup, fields = fields, many=True)
            serializer_data = serializer.data ## 시리얼라이즈 데이터
            data['data'] = serializer_data
            ##print(serializer_data)
        else:
            data['data'] = 'nodata'    
            
        
    json_data_call = json.dumps(data)
    return HttpResponse(json_data_call, content_type="applications/json")    
         
        
    # phnoegroup = PhoneGroup.objects.filter(measdate=toDate_str, ispId='45008')
    # context = {
    #         'phnoegroup' : phnoegroup
    # }
        
    # return render(request,"analysis/dashboard_form.html",context)

#FBV messagelist
def get_listview_m(request):
    """함수기반 뷰 FBV 메세지데이터 호출 뷰"""
    data = {}
    if request.method== "POST":
        
        group_id = request.POST['groupid']
        tab_check = request.POST['tabcheck']
        print("이거잘나오나:", group_id)
        ## ex) 1,2,3,4
        phone_group = PhoneGroup.objects.get(id = group_id)
        phones = phone_group.phone_set.all()
        ## 메세지 모델에 그룹아이디생성 임시로 
        
        if tab_check == 'event':
            message_data = Message.objects.filter(phone__in = phones, messageType='EVENT').order_by('-updated_at')
        elif tab_check == 'tele':
            message_data = Message.objects.filter(phone__in = phones, sendType='TELE', messageType='SMS').order_by('-updated_at')
        else:
            message_data = Message.objects.filter(phone__in = phones, sendType='XROSHOT').order_by('-updated_at')
            
        print(message_data)
        
        fields = ['create_time','phone_no_sht','message','sended_time','sended','status']
        #fields = ['create_time','phone_no_sht','message','sended_time','sended','status','isDel']

        if len(message_data) != 0:
            serializer = MessageSerializer(message_data, fields = fields, many=True)
            serializer_data = serializer.data ## 시리얼라이즈 데이터
            data['data'] = serializer_data
            #print(serializer_data)
        else:
            data['data'] = 'nodata'    
            
    json_data_call = json.dumps(data)
    return HttpResponse(json_data_call, content_type="applications/json") 


class PhoneGroupDetailView(TemplateView):
    """클래스 기반 뷰 CBV 그룹데이터 호출 뷰"""
    template_name = 'analysis/dashboard_form.html'
    def post(self, request, **kwargs):
        queryset = PhoneGroup.objects.all()
        ctx = {
            'data' :  queryset  
        } 
        return self.render_to_response(ctx)
    
    # def post_context_data(self, *args, **kwargs):
    #     context = super(PhoneGroupDetailView, self).post_context_data(*args, **kwargs)
    #     context['phonegroup'] = PhoneGroup.objects.all()
    #     return context
    
    # def get(self, request, *arg, **kwargs):
    #     if request.is_ajax():
    #         return super(PhoneGroupDetailView, self).get(request, *arg, **kwargs)
    
    # template_name = 'analysis/dashboard_form.html'
    # model = PhoneGroup.objects.all()

    

    

def get_startdata(request):
    """초기 데이터 호출 view 날짜를 전달받는다"""
    if request.method== "POST":

        toDate = request.POST['date'].split('-')
        toDate_str = "".join(toDate)

        print(toDate_str)
        
        start_dict = ajax_startdata(toDate_str) 
        json_data_call = json.dumps(start_dict)
        
    return HttpResponse(json_data_call, content_type="applications/json")

# -------------------------------------------------------------------------------------------------
# 홈페이지 페이지
# -------------------------------------------------------------------------------------------------
def dashboard(request):
    """홈(Home) 페이지 뷰"""
    if request.user.is_authenticated:
        
        return render(request, "analysis/dashboard_form.html")
    else:
        return redirect(reverse('accounts:login'))

# -------------------------------------------------------------------------------------------------
# 일일보고 페이지
# -------------------------------------------------------------------------------------------------
def report(request):
    """일일보고 페이지 뷰"""
    # 레포트에서 사용할 데이터(컨텍스트)를 가져온다.
    context = get_report_cntx()
    return render(request, "analysis/daily_report_form.html", context)

# -------------------------------------------------------------------------------------------------
# 대상등록 페이지 - 측정대상, 측정완료, 전년도결과, 추가기입사항
# -------------------------------------------------------------------------------------------------
def register_measdata(request):
    """ 대상등록 페이지 뷰
        - 등록대상 : 측정대상, 측정완료, 전년도결과(5G, LTE), 추가기입사항
    """
    context = get_measresult_cntx()
    return render(request, "analysis/register_measdata_form.html", context)

# -------------------------------------------------------------------------------------------------
# 측정대상 등록 및 수정
# -------------------------------------------------------------------------------------------------
def create_measplan(request):
    """ 측정대상 등록 및 수정 뷰"""
    # create_measplan()
    if request.method == "POST" :
        # POST 방식으로 데이터가 넘어오면 모델을 저장한다.
        updage__measplan(request)
    else:
        pass

    # return redirect("analysis:make_report")
    return redirect("analysis:register_measdata")


# -------------------------------------------------------------------------------------------------
# 측정대상 삭제
# -------------------------------------------------------------------------------------------------
def delete_measplan(request):
    """측정대상 등록정보를 삭제하는 뷰"""
    if request.method== "POST":
       # 측정대상 등록정보를 삭제한다.
       MeasPlan.objects.all().delete()

    return redirect("analysis:register_measdata")


# -------------------------------------------------------------------------------------------------
# 측정완료 등록 및 수정
# [ 의견사항 ]
# - 로직 검토가 필요 임의로 삭제하는 로직이 들어 가 있는데, 기존에 데이터가 있으면 보여주고,
#   사용자가 삭제할 수 있도록 하는 것이 바람직해 보임
# -------------------------------------------------------------------------------------------------
def create_measresult(request):
    """ 측정완료 등록 및 수정 뷰"""
    if request.method == "POST":

        measresult = MeasResult()

        measresult.date = request.POST['date']
        measresult.networkId = request.POST['networkId']
        measresult.measinfo = request.POST['measinfo']
        measresult.district = request.POST['district']
        measresult.area = request.POST['area']
        measresult.molph_level0 = request.POST['molph_level0']
        measresult.molph_level1 = request.POST['molph_level1']

        # 기존에 등록된 측정결과 데이터가 있으면 삭제한다.
        MeasResult.objects.filter(date=measresult.date, measinfo=measresult.measinfo).delete()

        # 측정결과를 저장한다.
        measresult.save()

    return redirect("analysis:register_measdata")


# -------------------------------------------------------------------------------------------------
# 6) 측정완료 삭제
# -------------------------------------------------------------------------------------------------
def delete_measresult(request):
    """측정결과 등록정보를 삭제하는 뷰"""
    if request.method== "POST":
       MeasResult.objects.all().delete()
      
    return redirect("analysis:register_measdata")


# -------------------------------------------------------------------------------------------------
# 추가사항 등록 및 수정
# -------------------------------------------------------------------------------------------------
def create_reportmsg(request):
    """ 추가기입사항 등록 및 수정 뷰"""
    if request.method == "POST":
        # 빈 객체를 생성한다.
        reportmsg = ReportMessage()

        reportmsg.msg5G = request.POST['msg5G']
        reportmsg.msgLTE = request.POST['msgLTE']
        reportmsg.msgWiFi = request.POST['msgWiFi']
        reportmsg.msgWeak = request.POST['msgWeak']
        reportmsg.msg5Gafter = request.POST['msg5Gafter']
        reportmsg.msgLTEafter = request.POST['msgLTEafter']

        ReportMessage.objects.all().delete()

        reportmsg.save()

    return redirect("analysis:register_measdata")

# -------------------------------------------------------------------------------------------------
# 추가사항 삭제
# -------------------------------------------------------------------------------------------------
def delete_reportmsg(request):
    """추가기입사항 등록정보를 삭제하는 뷰"""
    if request.method== "POST":
        ReportMessage.objects.all().delete()
       
    return redirect("analysis:register_measdata")

# -------------------------------------------------------------------------------------------------
# 전년도 결과 등록 및 수정(5G)
# [ 코드수점 검토사항 ]
# - MeaslastyearLTEDetailView로 이름 변경
# - 해당 뷰에서 신규/저장/삭제 기능이 모두 되게 기능을 넣는다.
# -------------------------------------------------------------------------------------------------
def create_measlastyear5G(request):
    """ 전년도 결과 등록 및 수정(5G) 뷰"""
    if request.method== "POST":
        # update_measlastyear5G(request)
        form = MeasLastyear5GForm(request.POST, request.FILES)
        if form.is_valid():
            measLastyear5G = form.save()
    else:
        # 데이터를 조회해서 화면에 넘겨주는 코드를 작성한다.
        pass

    return redirect("analysis:register_measdata")

# -------------------------------------------------------------------------------------------------
# 전년도 결과 삭제(5G)
# -------------------------------------------------------------------------------------------------
def delete_measlastyear5G(request):
    """전년도 결과(5G) 등록정보를 삭제하는 뷰"""
    if request.method== "POST":
        MeasLastyear5G.objects.all().delete()

    return redirect("analysis:register_measdata")

# -------------------------------------------------------------------------------------------------
# 전년도 결과 등록 및 수정(LTE)
# -------------------------------------------------------------------------------------------------
def create_measlastyearLTE(request):
    """ 전년도 결과 등록 및 수정(LTE) 뷰"""
    if request.method== "POST":
        # update_measlastyear5G(request)
        form = MeasLastyearLTEForm(request.POST, request.FILES)
        if form.is_valid():
            measLastyear5G = form.save()
    else:
        # 데이터를 조회해서 화면에 넘겨주는 코드를 작성한다.
        pass

    return redirect("analysis:register_measdata")

# -------------------------------------------------------------------------------------------------
# 전년도 결과 삭제(LTE)
# -------------------------------------------------------------------------------------------------
def delete_measlastyearLTE(request):
    """전년도 결과(LTE) 등록정보를 삭제하는 뷰"""
    if request.method== "POST":
       MeasLastyearLTE.objects.all().delete()

    return redirect("analysis:register_measdata")