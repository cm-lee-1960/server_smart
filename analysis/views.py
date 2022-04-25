# from django.shortcuts import render,redirect
# from django.contrib.auth.decorators import login_required
# from monitor.models import Phone
# from .models import MeasPlan, MeasResult,ReportMessage, MeasLastyear5G, MeasLastyearLTE
# import pandas as pd
# import datetime
# from django.db.models import Sum
# from makereport import *
# import sys
from django.db.models import Q
from multiprocessing.sharedctypes import Value
from operator import mod
from django.forms import CharField
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from monitor.models import Phone
from analysis.models import MeasPlan, MeasResult,ReportMessage, MeasLastyear5G, MeasLastyearLTE, PostMeasure5G
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
from monitor.serializers import MessageSerializer

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
        
        fields = ['create_time','phone_no_sht','message','sended_time','sended','status','isDel']
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


# class PhoneGroupDetailView(TemplateView):
#     """클래스 기반 뷰 CBV 그룹데이터 호출 뷰"""
#     template_name = 'analysis/dashboard_form.html'
#     def post(self, request, **kwargs):
#         queryset = PhoneGroup.objects.all()
#         ctx = {
#             'data' :  queryset
#         }
#         return self.render_to_response(ctx)
    
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
# 일일보고 대상등록 페이지
# -------------------------------------------------------------------------------------------------
def report_measplan(request):
    """일일보고 대상등록 페이지 뷰"""
    context = get_measresult_cntx(request)
    return render(request, "analysis/register_measplan_form.html", context)

# -------------------------------------------------------------------------------------------------
# 일일보고 리스트 페이지
# -------------------------------------------------------------------------------------------------
def report_list(request):
    """일일보고 대상등록 페이지 뷰"""
    context = get_measresult_cntx(request)
    return render(request, "analysis/daily_report_list.html", context)

# -------------------------------------------------------------------------------------------------
# 측정결과현황 페이지
# -------------------------------------------------------------------------------------------------
def report_measresult(request):
    """일일보고 대상등록 페이지 뷰"""
    context = get_measclose_cntx(request)
    return render(request, "analysis/register_measresult_form.html", context)



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
    return redirect("analysis:report_measplan")


# -------------------------------------------------------------------------------------------------
# 측정대상 삭제
# -------------------------------------------------------------------------------------------------
def delete_measplan(request):
    """측정대상 등록정보를 삭제하는 뷰"""
    if request.method== "POST":
       # 측정대상 등록정보를 삭제한다.
       MeasPlan.objects.all().delete()

    return redirect("analysis:report_measplan")


# -------------------------------------------------------------------------------------------------
# 측정완료 등록 및 수정
# [ 의견사항 ]
# - 로직 검토가 필요 임의로 삭제하는 로직이 들어 가 있는데, 기존에 데이터가 있으면 보여주고,
#   사용자가 삭제할 수 있도록 하는 것이 바람직해 보임
# -------------------------------------------------------------------------------------------------
def create_measresult(request):
    """ 측정완료 등록 및 수정 뷰"""
    if request.method == "POST":
        
      
        measresult1 = TestDayClose()
        measresult1.phoneGroup_id = request.POST['phoneGroup_id']
        measresult1.measdate = request.POST['measdate']
        measresult1.userInfo1 = request.POST['userInfo1']
        measresult1.networkId = request.POST['networkId']
        measresult1.district = request.POST['district']
        measresult1.mopo = request.POST['mopo']
        measresult1.address = request.POST['address']
        measresult1.downloadBandwidth = request.POST['downloadBandwidth']
        measresult1.uploadBandwidth = request.POST['uploadBandwidth']
        measresult1.lte_percent = request.POST['lte_percent']
        measresult1.success_rate = request.POST['success_rate']
        measresult1.connect_time = request.POST['connect_time']
        measresult1.udpJitter = request.POST['udpJitter']
        measresult1.plus = request.POST['plus']
        # 기존에 등록된 측정결과 데이터가 있으면 삭제한다.
        TestDayClose.objects.filter(phoneGroup_id=measresult1.phoneGroup_id, measdate=measresult1.measdate, userInfo1=measresult1.userInfo1).delete()

        # 측정결과를 저장한다.
        measresult1.save()

    return redirect("analysis:report_measresult")


# -------------------------------------------------------------------------------------------------
# 6) 측정완료 삭제
# -------------------------------------------------------------------------------------------------
def delete_measresult(request):
    """측정결과 등록정보를 삭제하는 뷰"""
    if request.method== "POST":
       MeasResult.objects.all().delete()
      
    return redirect("analysis:report_measresult")


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

    return redirect("analysis:report")

# -------------------------------------------------------------------------------------------------
# 추가사항 삭제
# -------------------------------------------------------------------------------------------------
def delete_reportmsg(request):
    """추가기입사항 등록정보를 삭제하는 뷰"""
    if request.method== "POST":
        ReportMessage.objects.all().delete()
       
    return redirect("analysis:report")
# -------------------------------------------------------------------------------------------------
# 사후측정 결과 등록 및 수정(5G)
# [ 코드수점 검토사항 ]
# - 해당 뷰에서 신규/저장/삭제 기능이 모두 되게 기능을 넣는다.
# -------------------------------------------------------------------------------------------------
# def create_postmeasure5G(request):
#     """ 전년도 결과 등록 및 수정(5G) 뷰"""
#     if request.method== "POST":
#         # update_postmeasure5G(request)
#         form = PostMeasure5GForm(request.POST, request.FILES)
#         if form.is_valid():
#             postmeasure5G = form.save()
#     else:
#         # 데이터를 조회해서 화면에 넘겨주는 코드를 작성한다.
#         pass

#     return redirect("analysis:report")
def create_postmeasure5G(request):
    if request.method == "POST":
        # 빈 객체를 생성한다.
        postmeas5G = PostMeasure5G()
        postmeas5G.lasttotal = request.POST['lasttotal']
        postmeas5G.lastseoul = request.POST['lastseoul']
        postmeas5G.lastincheon = request.POST['lastincheon']
        postmeas5G.lastulsan = request.POST['lastulsan']
        postmeas5G.lastdaegu = request.POST['lastdaegu']
        postmeas5G.lastgwangju = request.POST['lastgwangju']
        postmeas5G.lastdaejun = request.POST['lastdaejun']
        postmeas5G.lastgyunggi = request.POST['lastgyunggi']
        postmeas5G.lastgyungbuk = request.POST['lastgyungbuk']
        postmeas5G.lastjunnam = request.POST['lastjunnam']
        postmeas5G.lastjunbuk = request.POST['lastjunbuk']
        postmeas5G.lastchungnam = request.POST['lastchungnam']
        postmeas5G.lastchungbuk = request.POST['lastchungbuk']
        postmeas5G.lastsejong = request.POST['lastsejong']
        #KT 본 종합 결과
        postmeas5G.kttotaltotal = request.POST['kttotaltotal']
        postmeas5G.kttotalseoul = request.POST['kttotalseoul']
        postmeas5G.kttotalincheon = request.POST['kttotalincheon']
        postmeas5G.kttotalulsan = request.POST['kttotalulsan']
        postmeas5G.kttotaldaegu = request.POST['kttotaldaegu']
        postmeas5G.kttotalgwangju = request.POST['kttotalgwangju']
        postmeas5G.kttotaldaejun = request.POST['kttotaldaejun']
        postmeas5G.kttotalgyunggi = request.POST['kttotalgyunggi']
        postmeas5G.kttotalgyungbuk = request.POST['kttotalgyungbuk']
        postmeas5G.kttotaljunnam = request.POST['kttotaljunnam']
        postmeas5G.kttotaljunbuk = request.POST['kttotaljunbuk']
        postmeas5G.kttotalchungnam = request.POST['kttotalchungnam']
        postmeas5G.kttotalchungbuk = request.POST['kttotalchungbuk']
        postmeas5G.kttotalsejong = request.POST['kttotalsejong']
        #KT 사후 종합 결과
        postmeas5G.kttotalposttotal = request.POST['kttotalposttotal']
        postmeas5G.kttotalpostseoul = request.POST['kttotalpostseoul']
        postmeas5G.kttotalpostincheon = request.POST['kttotalpostincheon']
        postmeas5G.kttotalpostulsan = request.POST['kttotalpostulsan']
        postmeas5G.kttotalpostdaegu = request.POST['kttotalpostdaegu']
        postmeas5G.kttotalpostgwangju = request.POST['kttotalpostgwangju']
        postmeas5G.kttotalpostdaejun = request.POST['kttotalpostdaejun']
        postmeas5G.kttotalpostgyunggi = request.POST['kttotalpostgyunggi']
        postmeas5G.kttotalpostgyungbuk = request.POST['kttotalpostgyungbuk']
        postmeas5G.kttotalpostjunnam = request.POST['kttotalpostjunnam']
        postmeas5G.kttotalpostjunbuk = request.POST['kttotalpostjunbuk']
        postmeas5G.kttotalpostchungnam = request.POST['kttotalpostchungnam']
        postmeas5G.kttotalpostchungbuk = request.POST['kttotalpostchungbuk']
        postmeas5G.kttotalpostsejong = request.POST['kttotalpostsejong']
        #S사 사후 종합 결과
        postmeas5G.skttotalposttotal = request.POST['skttotalposttotal']
        postmeas5G.skttotalpostseoul = request.POST['skttotalpostseoul']
        postmeas5G.skttotalpostincheon = request.POST['skttotalpostincheon']
        postmeas5G.skttotalpostulsan = request.POST['skttotalpostulsan']
        postmeas5G.skttotalpostdaegu = request.POST['skttotalpostdaegu']
        postmeas5G.skttotalpostgwangju = request.POST['skttotalpostgwangju']
        postmeas5G.skttotalpostdaejun = request.POST['skttotalpostdaejun']
        postmeas5G.skttotalpostgyunggi = request.POST['skttotalpostgyunggi']
        postmeas5G.skttotalpostgyungbuk = request.POST['skttotalpostgyungbuk']
        postmeas5G.skttotalpostjunnam = request.POST['skttotalpostjunnam']
        postmeas5G.skttotalpostjunbuk = request.POST['skttotalpostjunbuk']
        postmeas5G.skttotalpostchungnam = request.POST['skttotalpostchungnam']
        postmeas5G.skttotalpostchungbuk = request.POST['skttotalpostchungbuk']
        postmeas5G.skttotalpostsejong = request.POST['skttotalpostsejong']
        #L사 사후 종합 결과
        postmeas5G.lgtotalposttotal=request.POST["lgtotalposttotal"]
        postmeas5G.lgtotalpostseoul=request.POST["lgtotalpostseoul"]
        postmeas5G.lgtotalpostincheon=request.POST["lgtotalpostincheon"]
        postmeas5G.lgtotalpostulsan=request.POST["lgtotalpostulsan"]
        postmeas5G.lgtotalpostdaegu=request.POST["lgtotalpostdaegu"]
        postmeas5G.lgtotalpostgwangju=request.POST["lgtotalpostgwangju"]
        postmeas5G.lgtotalpostdaejun=request.POST["lgtotalpostdaejun"]
        postmeas5G.lgtotalpostgyunggi=request.POST["lgtotalpostgyunggi"]
        postmeas5G.lgtotalpostgyungbuk=request.POST["lgtotalpostgyungbuk"]
        postmeas5G.lgtotalpostjunnam=request.POST["lgtotalpostjunnam"]
        postmeas5G.lgtotalpostjunbuk=request.POST["lgtotalpostjunbuk"]
        postmeas5G.lgtotalpostchungnam=request.POST["lgtotalpostchungnam"]
        postmeas5G.lgtotalpostchungbuk=request.POST["lgtotalpostchungbuk"]
        postmeas5G.lgtotalpostsejong=request.POST["lgtotalpostsejong"]
        #KT
        postmeas5G.kthjdtotal=request.POST["kthjdtotal"]
        postmeas5G.kthjdseoul=request.POST["kthjdseoul"]
        postmeas5G.kthjdincheon=request.POST["kthjdincheon"]
        postmeas5G.kthjdulsan=request.POST["kthjdulsan"]
        postmeas5G.kthjddaegu=request.POST["kthjddaegu"]
        postmeas5G.kthjdgwangju=request.POST["kthjdgwangju"]
        postmeas5G.kthjddaejun=request.POST["kthjddaejun"]
        postmeas5G.kthjdgyunggi=request.POST["kthjdgyunggi"]
        postmeas5G.kthjdgyungbuk=request.POST["kthjdgyungbuk"]
        postmeas5G.kthjdjunnam=request.POST["kthjdjunnam"]
        postmeas5G.kthjdjunbuk=request.POST["kthjdjunbuk"]
        postmeas5G.kthjdchungnam=request.POST["kthjdchungnam"]
        postmeas5G.kthjdchungbuk=request.POST["kthjdchungbuk"]
        postmeas5G.kthjdsejong=request.POST["kthjdsejong"]
        #KT
        postmeas5G.kthjdposttotal=request.POST["kthjdposttotal"]
        postmeas5G.kthjdpostseoul=request.POST["kthjdpostseoul"]
        postmeas5G.kthjdpostincheon=request.POST["kthjdpostincheon"]
        postmeas5G.kthjdpostulsan=request.POST["kthjdpostulsan"]
        postmeas5G.kthjdpostdaegu=request.POST["kthjdpostdaegu"]
        postmeas5G.kthjdpostgwangju=request.POST["kthjdpostgwangju"]
        postmeas5G.kthjdpostdaejun=request.POST["kthjdpostdaejun"]
        postmeas5G.kthjdpostgyunggi=request.POST["kthjdpostgyunggi"]
        postmeas5G.kthjdpostgyungbuk=request.POST["kthjdpostgyungbuk"]
        postmeas5G.kthjdpostjunnam=request.POST["kthjdpostjunnam"]
        postmeas5G.kthjdpostjunbuk=request.POST["kthjdpostjunbuk"]
        postmeas5G.kthjdpostchungnam=request.POST["kthjdpostchungnam"]
        postmeas5G.kthjdpostchungbuk=request.POST["kthjdpostchungbuk"]
        postmeas5G.kthjdpostsejong=request.POST["kthjdpostsejong"]
        #S사
        postmeas5G.skthjdposttotal=request.POST["skthjdposttotal"]
        postmeas5G.skthjdpostseoul=request.POST["skthjdpostseoul"]
        postmeas5G.skthjdpostincheon=request.POST["skthjdpostincheon"]
        postmeas5G.skthjdpostulsan=request.POST["skthjdpostulsan"]
        postmeas5G.skthjdpostdaegu=request.POST["skthjdpostdaegu"]
        postmeas5G.skthjdpostgwangju=request.POST["skthjdpostgwangju"]
        postmeas5G.skthjdpostdaejun=request.POST["skthjdpostdaejun"]
        postmeas5G.skthjdpostgyunggi=request.POST["skthjdpostgyunggi"]
        postmeas5G.skthjdpostgyungbuk=request.POST["skthjdpostgyungbuk"]
        postmeas5G.skthjdpostjunnam=request.POST["skthjdpostjunnam"]
        postmeas5G.skthjdpostjunbuk=request.POST["skthjdpostjunbuk"]
        postmeas5G.skthjdpostchungnam=request.POST["skthjdpostchungnam"]
        postmeas5G.skthjdpostchungbuk=request.POST["skthjdpostchungbuk"]
        postmeas5G.skthjdpostsejong=request.POST["skthjdpostsejong"]
        #L사
        postmeas5G.lghjdposttotal=request.POST["lghjdposttotal"]
        postmeas5G.lghjdpostseoul=request.POST["lghjdpostseoul"]
        postmeas5G.lghjdpostincheon=request.POST["lghjdpostincheon"]
        postmeas5G.lghjdpostulsan=request.POST["lghjdpostulsan"]
        postmeas5G.lghjdpostdaegu=request.POST["lghjdpostdaegu"]
        postmeas5G.lghjdpostgwangju=request.POST["lghjdpostgwangju"]
        postmeas5G.lghjdpostdaejun=request.POST["lghjdpostdaejun"]
        postmeas5G.lghjdpostgyunggi=request.POST["lghjdpostgyunggi"]
        postmeas5G.lghjdpostgyungbuk=request.POST["lghjdpostgyungbuk"]
        postmeas5G.lghjdpostjunnam=request.POST["lghjdpostjunnam"]
        postmeas5G.lghjdpostjunbuk=request.POST["lghjdpostjunbuk"]
        postmeas5G.lghjdpostchungnam=request.POST["lghjdpostchungnam"]
        postmeas5G.lghjdpostchungbuk=request.POST["lghjdpostchungbuk"]
        postmeas5G.lghjdpostsejong=request.POST["lghjdpostsejong"]
        #KT
        postmeas5G.ktsidetotal=request.POST["ktsidetotal"]
        postmeas5G.ktsideseoul=request.POST["ktsideseoul"]
        postmeas5G.ktsideincheon=request.POST["ktsideincheon"]
        postmeas5G.ktsideulsan=request.POST["ktsideulsan"]
        postmeas5G.ktsidedaegu=request.POST["ktsidedaegu"]
        postmeas5G.ktsidegwangju=request.POST["ktsidegwangju"]
        postmeas5G.ktsidedaejun=request.POST["ktsidedaejun"]
        postmeas5G.ktsidegyunggi=request.POST["ktsidegyunggi"]
        postmeas5G.ktsidegyungbuk=request.POST["ktsidegyungbuk"]
        postmeas5G.ktsidejunnam=request.POST["ktsidejunnam"]
        postmeas5G.ktsidejunbuk=request.POST["ktsidejunbuk"]
        postmeas5G.ktsidechungnam=request.POST["ktsidechungnam"]
        postmeas5G.ktsidechungbuk=request.POST["ktsidechungbuk"]
        postmeas5G.ktsidesejong=request.POST["ktsidesejong"]
        #KT
        postmeas5G.ktsideposttotal=request.POST["ktsideposttotal"]
        postmeas5G.ktsidepostseoul=request.POST["ktsidepostseoul"]
        postmeas5G.ktsidepostincheon=request.POST["ktsidepostincheon"]
        postmeas5G.ktsidepostulsan=request.POST["ktsidepostulsan"]
        postmeas5G.ktsidepostdaegu=request.POST["ktsidepostdaegu"]
        postmeas5G.ktsidepostgwangju=request.POST["ktsidepostgwangju"]
        postmeas5G.ktsidepostdaejun=request.POST["ktsidepostdaejun"]
        postmeas5G.ktsidepostgyunggi=request.POST["ktsidepostgyunggi"]
        postmeas5G.ktsidepostgyungbuk=request.POST["ktsidepostgyungbuk"]
        postmeas5G.ktsidepostjunnam=request.POST["ktsidepostjunnam"]
        postmeas5G.ktsidepostjunbuk=request.POST["ktsidepostjunbuk"]
        postmeas5G.ktsidepostchungnam=request.POST["ktsidepostchungnam"]
        postmeas5G.ktsidepostchungbuk=request.POST["ktsidepostchungbuk"]
        postmeas5G.ktsidepostsejong=request.POST["ktsidepostsejong"]
        #S사
        postmeas5G.sktsideposttotal=request.POST["sktsideposttotal"]
        postmeas5G.sktsidepostseoul=request.POST["sktsidepostseoul"]
        postmeas5G.sktsidepostincheon=request.POST["sktsidepostincheon"]
        postmeas5G.sktsidepostulsan=request.POST["sktsidepostulsan"]
        postmeas5G.sktsidepostdaegu=request.POST["sktsidepostdaegu"]
        postmeas5G.sktsidepostgwangju=request.POST["sktsidepostgwangju"]
        postmeas5G.sktsidepostdaejun=request.POST["sktsidepostdaejun"]
        postmeas5G.sktsidepostgyunggi=request.POST["sktsidepostgyunggi"]
        postmeas5G.sktsidepostgyungbuk=request.POST["sktsidepostgyungbuk"]
        postmeas5G.sktsidepostjunnam=request.POST["sktsidepostjunnam"]
        postmeas5G.sktsidepostjunbuk=request.POST["sktsidepostjunbuk"]
        postmeas5G.sktsidepostchungnam=request.POST["sktsidepostchungnam"]
        postmeas5G.sktsidepostchungbuk=request.POST["sktsidepostchungbuk"]
        postmeas5G.sktsidepostsejong=request.POST["sktsidepostsejong"]
        #L사
        postmeas5G.lgsideposttotal=request.POST["lgsideposttotal"]
        postmeas5G.lgsidepostseoul=request.POST["lgsidepostseoul"]
        postmeas5G.lgsidepostincheon=request.POST["lgsidepostincheon"]
        postmeas5G.lgsidepostulsan=request.POST["lgsidepostulsan"]
        postmeas5G.lgsidepostdaegu=request.POST["lgsidepostdaegu"]
        postmeas5G.lgsidepostgwangju=request.POST["lgsidepostgwangju"]
        postmeas5G.lgsidepostdaejun=request.POST["lgsidepostdaejun"]
        postmeas5G.lgsidepostgyunggi=request.POST["lgsidepostgyunggi"]
        postmeas5G.lgsidepostgyungbuk=request.POST["lgsidepostgyungbuk"]
        postmeas5G.lgsidepostjunnam=request.POST["lgsidepostjunnam"]
        postmeas5G.lgsidepostjunbuk=request.POST["lgsidepostjunbuk"]
        postmeas5G.lgsidepostchungnam=request.POST["lgsidepostchungnam"]
        postmeas5G.lgsidepostchungbuk=request.POST["lgsidepostchungbuk"]
        postmeas5G.lgsidepostsejong=request.POST["lgsidepostsejong"]
        #KT
        postmeas5G.ktranktotal=request.POST["ktranktotal"]
        postmeas5G.ktrankseoul=request.POST["ktrankseoul"]
        postmeas5G.ktrankincheon=request.POST["ktrankincheon"]
        postmeas5G.ktrankulsan=request.POST["ktrankulsan"]
        postmeas5G.ktrankdaegu=request.POST["ktrankdaegu"]
        postmeas5G.ktrankgwangju=request.POST["ktrankgwangju"]
        postmeas5G.ktrankdaejun=request.POST["ktrankdaejun"]
        postmeas5G.ktrankgyunggi=request.POST["ktrankgyunggi"]
        postmeas5G.ktrankgyungbuk=request.POST["ktrankgyungbuk"]
        postmeas5G.ktrankjunnam=request.POST["ktrankjunnam"]
        postmeas5G.ktrankjunbuk=request.POST["ktrankjunbuk"]
        postmeas5G.ktrankchungnam=request.POST["ktrankchungnam"]
        postmeas5G.ktrankchungbuk=request.POST["ktrankchungbuk"]
        postmeas5G.ktranksejong=request.POST["ktranksejong"]
        #KT
        postmeas5G.ktrankhjdtotal=request.POST["ktrankhjdtotal"]
        postmeas5G.ktrankhjdseoul=request.POST["ktrankhjdseoul"]
        postmeas5G.ktrankhjdincheon=request.POST["ktrankhjdincheon"]
        postmeas5G.ktrankhjdulsan=request.POST["ktrankhjdulsan"]
        postmeas5G.ktrankhjddaegu=request.POST["ktrankhjddaegu"]
        postmeas5G.ktrankhjdgwangju=request.POST["ktrankhjdgwangju"]
        postmeas5G.ktrankhjddaejun=request.POST["ktrankhjddaejun"]
        postmeas5G.ktrankhjdgyunggi=request.POST["ktrankhjdgyunggi"]
        postmeas5G.ktrankhjdgyungbuk=request.POST["ktrankhjdgyungbuk"]
        postmeas5G.ktrankhjdjunnam=request.POST["ktrankhjdjunnam"]
        postmeas5G.ktrankhjdjunbuk=request.POST["ktrankhjdjunbuk"]
        postmeas5G.ktrankhjdchungnam=request.POST["ktrankhjdchungnam"]
        postmeas5G.ktrankhjdchungbuk=request.POST["ktrankhjdchungbuk"]
        postmeas5G.ktrankhjdsejong=request.POST["ktrankhjdsejong"]

        #KT 다중이용시설/교통/아파트/대학 순위
        postmeas5G.ktranksidetotal = request.POST['ktranksidetotal']
        postmeas5G.ktranksideseoul = request.POST['ktranksideseoul']
        postmeas5G.ktranksideincheon = request.POST['ktranksideincheon']
        postmeas5G.ktranksideulsan = request.POST['ktranksideulsan']
        postmeas5G.ktranksidedaegu = request.POST['ktranksidedaegu']
        postmeas5G.ktranksidegwangju = request.POST['ktranksidegwangju']
        postmeas5G.ktranksidedaejun = request.POST['ktranksidedaejun']
        postmeas5G.ktranksidegyunggi = request.POST['ktranksidegyunggi']
        postmeas5G.ktranksidegyungbuk = request.POST['ktranksidegyungbuk']
        postmeas5G.ktranksidejunnam = request.POST['ktranksidejunnam']
        postmeas5G.ktranksidejunbuk = request.POST['ktranksidejunbuk']
        postmeas5G.ktranksidechungnam = request.POST['ktranksidechungnam']
        postmeas5G.ktranksidechungbuk = request.POST['ktranksidechungbuk']
        postmeas5G.ktranksidesejong = request.POST['ktranksidesejong']


        PostMeasure5G.objects.all().delete()

        postmeas5G.save()

    return redirect("analysis:report")


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