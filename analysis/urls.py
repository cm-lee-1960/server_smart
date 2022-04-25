from django.urls import path
from . import views
from .views import *
app_name = 'analysis'
urlpatterns = [
                                        
    path('dashboard/',views.dashboard,name='dashboard'), # 홈 화면
    path("report/", views.report, name='report'), # 일일보고 페이지

   # 추가사항(필요없는것은 삭제예정)
    
    path("report/measplan/", views.report_measplan, name='report_measplan'), # 측정대상등록 페이지
    path("report/list/", views.report_list, name='report_list'), # 일일보고 리스트 페이지
    path("report/measresult/", views.report_measresult, name='report_measresult'), # 측정결과현황 페이지
    

    path('report/makereport/', views.register_measdata, name='register_measdata'), # 레포트정보등록페이지(측정대상, 측정완료, 전년도결과, 추가사항)
    path('measplan/create/',views.create_measplan,name='create_measplan'), # 측정대상 등록 및 수정
    path('measplan/delete/',views.delete_measplan,name='delete_measplan'), # 측정대상 삭제
    path('measresult/create/',views.create_measresult,name='create_measresult'), # 측정완료 등록 및 수정
    path('measresult/delete/',views.delete_measresult,name='delete_measresult'), # 측정완료 삭제
    path('reportmsg/create/',views.create_reportmsg,name='create_reportmsg'), # 추가사항 등록 및 수정
    path('reportmsg/delete/',views.delete_reportmsg,name='delete_reportmsg'), # 추가사항 삭제
    path('measlastyear5G/create/',views.create_measlastyear5G,name='create_measlastyear5G'), # 전년도 결과 등록 및 수정(5G)
    path('measlastyear5G/delete/',views.delete_measlastyear5G,name='delete_measlastyear5G'), # 전년도 결과 삭제(5G)
    path('measlastyearLTE/create/',views.create_measlastyearLTE,name='create_measlastyearLTE'), # 전년도 결과 등록 및 수정(LTE)
    path('measlastyearLTE/delete/',views.delete_measlastyearLTE,name='delete_measlastyearLTE'), # 전년도 결과 삭제(LTE)
    path('postmeasure5G/create/',views.create_postmeasure5G,name='create_postmeasure5G'), # 사후측정 결과 등록 및 수정(LTE)
    
    
    # #ajax url
    # path('ajax/getstartdata/', views.get_startdata, name='ajax_startdata'), ## 초기데이터 가져온다(오늘의 측정)
    # path('listview/phoneGroupData/', views.get_listview, name='listview_phoneGroupData'), ## ## 측정그룹데이터가져온다(금일 측정그룹)
    # path('listview/messageData/', views.get_listview_m, name='listview_messageData')
    
    #view url
    ## ## 측정그룹데이터가져온다(금일 측정그룹)
    #path('listview/phoneGroupData/', views.PhoneGroupDetailView.as_view(), name='listview_phoneGroupData')
]
