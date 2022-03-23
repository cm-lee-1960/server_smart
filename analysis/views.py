# from django.shortcuts import render,redirect
# from django.contrib.auth.decorators import login_required
# from monitor.models import Phone
# from .models import MeasPlan, MeasResult,ReportMessage, MeasLastyear5G, MeasLastyearLTE
# import pandas as pd
# import datetime
# from django.db.models import Sum
# from makereport import *
# import sys

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from monitor.models import Phone
from analysis.models import MeasPlan, MeasResult,ReportMessage, MeasLastyear5G, MeasLastyearLTE
import pandas as pd
import datetime
from django.db.models import Sum
from .makereport import *

###################################################################################################
# 분석 처리모듈
# -------------------------------------------------------------------------------------------------
# 2022-03-23 - 모듈 정리 및 주석 추가
###################################################################################################

# -------------------------------------------------------------------------------------------------
# 홈(Home) 페이지
# -------------------------------------------------------------------------------------------------
def dashboard_form(request):
    """홈(Home) 페이지 뷰"""
    return render(request, "analysis/dashboard_form.html")

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
    if(request.method== "POST") :
        updage__measplan(request)

    # return redirect("analysis:make_report")
    return redirect("analysis:make_report")


# -------------------------------------------------------------------------------------------------
# 측정대상 삭제
# -------------------------------------------------------------------------------------------------
def delete_measplan(request):
    if(request.method== "POST") :
       
       MeasPlan.objects.all().delete()

    return redirect("analysis:register_measdata")

# -------------------------------------------------------------------------------------------------
# 측정완료 등록 및 수정
# -------------------------------------------------------------------------------------------------
def create_measresult(request):
    create_measresult(request)

# -------------------------------------------------------------------------------------------------
# 6) 측정완료 삭제
# -------------------------------------------------------------------------------------------------
def delete_measresult(request):
    if(request.method== "POST") :
       
       MeasResult.objects.all().delete()
      
    return redirect("analysis:delete_measresult")


# -------------------------------------------------------------------------------------------------
# 추가사항 등록 및 수정
# -------------------------------------------------------------------------------------------------
def create_reportmsg(request):
    create_reportmsg(request)


# -------------------------------------------------------------------------------------------------
# 추가사항 삭제
# -------------------------------------------------------------------------------------------------
def delete_reportmsg(request):
    if(request.method== "POST") :
       
        ReportMessage.objects.all().delete()
       
    return redirect("analysis:delete_reportmsg")

# -------------------------------------------------------------------------------------------------
# 전년도 결과 등록 및 수정(5G)
# -------------------------------------------------------------------------------------------------
def create_measlastyear5G(request):
    create_measlastyear5G(request)

# -------------------------------------------------------------------------------------------------
# 전년도 결과 삭제(5G)
# -------------------------------------------------------------------------------------------------
def delete_measlastyear5G(request):
    if(request.method== "POST") :
       
        MeasLastyear5G.objects.all().delete()
       
    return redirect("analysis:delete_measlastyear5G")

# -------------------------------------------------------------------------------------------------
# 전년도 결과 등록 및 수정(LTE)
# -------------------------------------------------------------------------------------------------
def create_measlastyearLTE(request):
    create_measlastyearLTE(request)

# -------------------------------------------------------------------------------------------------
# 전년도 결과 삭제(LTE)
# -------------------------------------------------------------------------------------------------
def delete_measlastyearLTE(request):
    if(request.method== "POST") :
       
       MeasLastyearLTE.objects.all().delete()
       
    return redirect("analysis:delete_measlastyearLTE")

