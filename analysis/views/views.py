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


# 홈 화면
def dashboard_form(request):

    return render(request, "analysis/dashboard_form.html")

# 일일보고 페이지``
def report(request):
    report(request)

# 레포트정보등록페이지(측정대상, 측정완료, 전년도결과, 추가사항)
def make_report(request):
    make_report(request)

# 측정대상 등록 및 수정
def create_measplan(request):
    create_measplan()

# 측정대상 삭제
def delete_measplan(request):
    if(request.method== "POST") :
       
       MeasPlan.objects.all().delete()

    return redirect("analysis:delete_measplan")

# 측정완료 등록 및 수정
def create_measresult(request):
    create_measresult(request)

# 측정완료 삭제
def delete_measresult(request):
    if(request.method== "POST") :
       
       MeasResult.objects.all().delete()
      
    return redirect("analysis:delete_measresult")

# 추가사항 등록 및 수정
def create_reportmsg(request):
    create_reportmsg(request)

# 추가사항 삭제
def delete_reportmsg(request):
    if(request.method== "POST") :
       
        ReportMessage.objects.all().delete()
       
    return redirect("analysis:delete_reportmsg")

# 전년도 결과 등록 및 수정(5G)
def create_measlastyear5G(request):
    create_measlastyear5G(request)

# 전년도 결과 삭제(5G)
def delete_measlastyear5G(request):
    if(request.method== "POST") :
       
        MeasLastyear5G.objects.all().delete()
       
    return redirect("analysis:delete_measlastyear5G")

# 전년도 결과 등록 및 수정(LTE)
def create_measlastyearLTE(request):
    create_measlastyearLTE(request)

# 전년도 결과 삭제(LTE)
def delete_measlastyearLTE(request):
    if(request.method== "POST") :
       
       MeasLastyearLTE.objects.all().delete()
       
    return redirect("analysis:delete_measlastyearLTE")

