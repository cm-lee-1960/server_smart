from django.urls import path
from . import views

app_name = 'analysis'
urlpatterns = [
                                        
    path('dashboard/',views.dashboard,name='dashboard'), # 홈 화면
    path("report/", views.report, name='report'), # 일일보고 페이지

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
    
    #ajax url
    path('ajax/getstartdata/', views.get_startdata, name='ajax_startdata'), ## 초기데이터 가져온다(오늘의 측정)
    
    #view url
    path('listview/phoneGroupData/', views.get_listview, name='listview_phoneGroupData'), ## ## 측정그룹데이터가져온다(금일 측정그룹)
]
