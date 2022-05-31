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
from analysis.models import *
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
from django.http import Http404, HttpRequest, HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from .ajax import *

from django.views.generic import ListView
from django.shortcuts import get_list_or_404
from django.views.generic import TemplateView
from monitor.serializers import MessageSerializer
from PyPDF2 import PdfFileReader, PdfFileMerger#피디에프병합
import openpyxl#엑셀업로드
from django.views.generic import View
from rest_framework.decorators import api_view
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
        ##return render(request, "analysis/test.html")
    else:
        return redirect(reverse('accounts:login'))

# -------------------------------------------------------------------------------------------------
# 홈페이지 페이지(테스트)
# -------------------------------------------------------------------------------------------------
def dashboard_test(request):
    """홈(Home) 페이지 뷰"""
    if request.user.is_authenticated:

        return render(request, "analysis/dashboard_form_test.html")
    else:
        return redirect(reverse('accounts:login'))



#####################################################################################################
#PDF 병합
#####################################################################################################

def pdf_merge(request):
    # merger라는 이름의 pdf병합기를 준비
    merger = PdfFileMerger()

    # 준비한 파일들을 하나씩 읽은 후, merger에 추가
    merger.append(PdfFileReader(open("C:/Users/82109/Downloads/test.pdf", 'rb')))
    merger.append(PdfFileReader(open("C:/Users/82109/Downloads/test (1).pdf", 'rb')))
    merger.append(PdfFileReader(open("C:/Users/82109/Downloads/test (2).pdf", 'rb')))


    # merger가 새 pdf파일로 저장
    merger.write("C:/Users/82109/Downloads/testone.pdf")
    response = {'status': 1, 'message': '엑셀파일이 정상적으로 업로드 됐습니다.'}
    return HttpResponse(json.dumps(response), content_type='application/json')


################################################################################################
# 엑셀업로드테스트
#################################################################################################
#views.py

class ExcelUploadView5g(View):
    def post(self, request):
        excelFile = request.FILES['file']

        excel = openpyxl.load_workbook(excelFile, data_only=True)
        work_sheet = excel.worksheets[0]

        all_values = []
        for i, row in enumerate (work_sheet.rows):
            if i != 0 :
                row_value = []
                for cell in row:
                    row_value.append(cell.value)
                all_values.append(row_value)
            
        PostMeasure5G.objects.all().delete()
        for row in all_values:
            sample_model = PostMeasure5G(district = row[0],number = row[1],lasttotal5g = row[2],kttotaltotal5g = row[3],kttotalposttotal5g = row[4],skttotalposttotal5g = row[5],lgtotalposttotal5g =row[6],ktranktotal5g = row[7],
            kthjdtotal5g = row[8],kthjdposttotal5g = row[9],skthjdposttotal5g = row[10],lghjdposttotal5g = row[11],ktrankhjdtotal5g =row[12], ktsidetotal5g = row[13],ktsideposttotal5g = row[14],sktsideposttotal5g = row[15],lgsideposttotal5g = row[16],
            ktranksidetotal5g = row[17])
            
            sample_model.save()

        response = {'status': 1, 'message': '엑셀파일이 정상적으로 업로드 됐습니다.'}
        return HttpResponse(json.dumps(response), content_type='application/json')

class ExcelUploadViewlte(View):
    def post(self, request):
        excelFile = request.FILES['file']

        excel = openpyxl.load_workbook(excelFile, data_only=True)
        work_sheet = excel.worksheets[0]

        all_values = []
        for i, row in enumerate (work_sheet.rows):
            if i != 0 :
                row_value = []
                for cell in row:
                    row_value.append(cell.value)
                all_values.append(row_value)
         
        PostMeasureLTE.objects.all().delete()
        for row in all_values:
            sample_model = PostMeasureLTE(district = row[0],number = row[1],lasttotallte = row[2],ktdllte = row[3], ktpostdllte = row[4],sktpostdllte = row[5],lgpostdllte = row[6],ktullte =row[7],ktpostullte = row[8],
            sktpostullte = row[9],lgpostullte = row[10])
            
            sample_model.save()

        response = {'status': 1, 'message': '엑셀파일이 정상적으로 업로드 됐습니다.'}
        return HttpResponse(json.dumps(response), content_type='application/json')
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
    context = get_measplan_cntx(request)
    return render(request, "analysis/register_measplan_form.html", context)

# -------------------------------------------------------------------------------------------------
# 일일보고 리스트 페이지
# -------------------------------------------------------------------------------------------------
def report_list(request):
    """일일보고 대상등록 페이지 뷰"""
    context = {}
    return render(request, "analysis/daily_report_list.html", context)

# -------------------------------------------------------------------------------------------------
# 측정결과현황 페이지
# -------------------------------------------------------------------------------------------------
def report_measresult(request):
    """일일보고 대상등록 페이지 뷰"""
    context = get_measclose_cntx(request)
    
    return render(request, "analysis/register_measresult_form.html", context)

# -------------------------------------------------------------------------------------------------
# 사후측정등록 페이지
# -------------------------------------------------------------------------------------------------
def report_postmeas(request):
    """일일보고 대상등록 페이지 뷰"""
    context = get_report_cntx()
    return render(request, "analysis/register_postmeas_form.html", context)



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
###########
#ajax 테스트
#####
###################
#마감데이터 등록 및 수정
####################
@api_view(['POST'])
def update_closedata(request):
    if request.method == "POST":
        """ 대쉬보드에서 단말그룹 더블클릭하여 정보 수정할 때 함수
        반환값: {result : 'ok' / 'fail'} """
        data = request.data
        data_len = data['select_tr']
        try:
            closedata = LastMeasDayClose.objects.filter(phoneGroup=int(data['select_tr'][0]),measdate=data['select_tr'][1],userInfo1=data['select_tr'][2])
            # if closedata.exists():
               
            closedata.phoneGroup = int(data_len[0])
            closedata.measdate = data_len[1]
            closedata.userInfo1 = data_len[2]
            closedata.nettype = data_len[3]
            closedata.center = data_len[4]
            closedata.mopho = data_len[5]
            closedata.district = data_len[6]
            closedata.guGun = data_len[7]
            closedata.detailadd = data_len[8]
            closedata.downloadBandwidth = float(data_len[9])
            closedata.uploadBandwidth = float(data_len[10])
            closedata.lte_percent =float(data_len[11])
            closedata.success_rate = float(data_len[12])
            closedata.connect_time = float(data_len[13])
            closedata.udpJitter = float(data_len[14])
            closedata.subadd = data_len[14]
            # 기존에 등록된 측정결과 데이터가 있으면 삭제한다.
            LastMeasDayClose.objects.filter(phoneGroup=int(data['select_tr'][0]),measdate=data['select_tr'][1],userInfo1=data['select_tr'][2]).delete()
            # 측정결과를 저장한다.
            closedata.save()
           
            result = {'result' : 'ok',}
            print("존재") 
            # else:
            #     print("존재X")
            #     closedata_new = LastMeasDayClose.objects.create( 
            #         phoneGroup_id = int(data_len[0]),
            #         measdate = data_len[1],
            #         userInfo1 = data_len[2],
            #         networkId = data_len[3],
            #         Center = data_len[4],
            #         Morphology = data_len[5],
            #         district = data_len[6],
            #         mopho = data_len[7],
            #         downloadBandwidth = float(data_len[8]),
            #         uploadBandwidth = float(data_len[9]),
            #         lte_percent =float(data_len[10]),
            #         success_rate = float(data_len[11]),
            #         connect_time = float(data_len[12]),
            #         udpJitter = float(data_len[13]),
            #         plus = data_len[14]
            #     )
    
            #     result = {'result' : 'ok',}
            #         ###############
            
        
        except Exception as e:
           
            closedata_new = LastMeasDayClose.objects.create( 
                phoneGroup = int(data_len[0]),
                measdate = data_len[1],
                userInfo1 = data_len[2],
                nettype = data_len[3],
                center = data_len[4],
                mopho = data_len[5],
                district = data_len[6],
                guGun = data_len[7],
                detailadd = data_len[8],
                downloadBandwidth = float(data_len[9]),
                uploadBandwidth = float(data_len[10]),
                lte_percent =float(data_len[11]),
                success_rate = float(data_len[12]),
                connect_time = float(data_len[13]),
                udpJitter = float(data_len[14]),
                subadd = data_len[15]
            )
  
            result = {'result' : 'ok',}
                ###############
        
            print("존재X")
            
            
            
            # print("에러.")
            # # 오류 코드 및 내용을 반환한다.
            # result = {'result' : 'fail'}

             
            
            
            
    return JsonResponse(data=result, safe=False)


###################
#마감데이터 삭제
####################
@api_view(['POST'])
def delete_closedata(request):
    if request.method == "POST":
        """ 대쉬보드에서 단말그룹 더블클릭하여 정보 수정할 때 함수
        반환값: {result : 'ok' / 'fail'} """
        data = request.data
        data_len = data['select_tr']
        try:
            print("존재")    
            LastMeasDayClose.objects.filter(phoneGroup=int(data['select_tr'][0]),measdate=data['select_tr'][1],userInfo1=data['select_tr'][2],nettype=data['select_tr'][3],center=data['select_tr'][4],mopho=data['select_tr'][5],district=data['select_tr'][6],guGun=data['select_tr'][7],detailadd=data['select_tr'][8]).delete()
            result = {'result' : 'ok',}
    
        
        except Exception as e:
            print("에러.")
            # 오류 코드 및 내용을 반환한다.
            result = {'result' : 'fail'}
        
            
            
            
            
            # print("에러.")
            # # 오류 코드 및 내용을 반환한다.
            # result = {'result' : 'fail'}

            
            
            
            
    return JsonResponse(data=result, safe=False)

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

def create_postmeasure5G(request):
    if request.method == "POST":
        # 빈 객체를 생성한다.
        postmeas = PostMeasure5G()
        postmeas.district = request.POST['district']
        postmeas.lasttotal5g = request.POST['lasttotal5g']
        postmeas.kttotaltotal5g = request.POST['kttotaltotal5g']
        postmeas.kttotalposttotal5g = request.POST['kttotalposttotal5g']
        postmeas.skttotalposttotal5g = request.POST['skttotalposttotal5g']
        postmeas.lgtotalposttotal5g = request.POST['lgtotalposttotal5g']
        postmeas.kthjdtotal5g = request.POST['kthjdtotal5g']
        postmeas.kthjdposttotal5g = request.POST['kthjdposttotal5g']
        postmeas.skthjdposttotal5g = request.POST['skthjdposttotal5g']
        postmeas.lghjdposttotal5g = request.POST['lghjdposttotal5g']
        postmeas.ktsidetotal5g = request.POST['ktsidetotal5g']
        postmeas.ktsideposttotal5g = request.POST['ktsideposttotal5g']
        postmeas.sktsideposttotal5g = request.POST['sktsideposttotal5g']
        postmeas.lgsideposttotal5g = request.POST['lgsideposttotal5g']
        postmeas.ktranktotal5g = request.POST['ktranktotal5g']
        postmeas.ktrankhjdtotal5g = request.POST['ktrankhjdtotal5g']
        postmeas.ktranksidetotal5g = request.POST['ktranksidetotal5g']
     
        
        PostMeasure5G.objects.all().delete()

        postmeas.save()

    return redirect("analysis:report")


def create_postmeasureLTE(request):
    if request.method == "POST":
        # 빈 객체를 생성한다.
        postmeas = PostMeasureLTE()
        postmeas.district = request.POST['district']
        
        postmeas.lasttotallte = request.POST['lasttotallte']
        postmeas.ktdllte = request.POST['ktdllte']
        postmeas.ktpostdllte = request.POST['ktpostdllte']
        postmeas.sktpostdllte = request.POST['sktpostdllte']
        postmeas.lgpostdllte = request.POST['lgpostdllte']
        postmeas.ktullte = request.POST['ktullte']
        postmeas.ktpostullte = request.POST['ktpostullte']
        postmeas.sktpostullte = request.POST['sktpostullte']
        postmeas.lgpostullte = request.POST['lgpostullte']
        
        PostMeasureLTE.objects.all().delete()

        postmeas.save()

    return redirect("analysis:report")
      



# ----------------------------------------------------------------------------------------------------------------------
# 측정마감데이터 조회 API
# ----------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def closedata_list(request, measdate):
    # 측정일자가 파라미터로 넘어오지 않는 경우 현재 날짜로 측정일자를 설정한다.
    if measdate is not None:
        # 측정일자에서 데시(-)를 제거한다(2021-11-01 -> 20211101).
        measdate = measdate.replace('-', '')
    else:
        # 측정일자를 널(Null)인 경우 현재 일자로 설정한다.
       measdate = datetime.now().strftime("%Y%m%d")

    try:
        # 해당 측정일자에 대한 단말그룹 정보를 가져온다.
        measclose = LastMeasDayClose.objects.filter(measdate=measdate, manage=True).order_by('-last_updated_dt')
        
        if measclose.exists():
            context = {'measclose':measclose}
            return render(request, "analysis/register_measresult_form.html", context)
        

    except Exception as e:
        print("closedata_list():", str(e))
        # db_logger.error("phonegroup_list(): %s" % e)
        raise Exception("closedata_list(): %s" % e)

    # 해당일자 총 측정건수, 센터별 측정건수, 단말그룹 정보를 JSON 데이터로 넘겨준다.
    


       


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