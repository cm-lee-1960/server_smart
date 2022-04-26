from django.urls import path
from . import views

app_name = 'monitor'
urlpatterns = [
    path("json/", views.receive_json), # 측정 데이터 처리
    path("end/<int:phonegroup_id>", views.measuring_end_view, name='measuring_end'), # 측정종료
    path("end/cancel/<int:phonegroup_id>", views.measuring_end_cancel_view), # 측정종료 취소
    path("end/union/<int:phonegroup_id>", views.phonegroup_union_view), # 폰그룹 합치기
    path("close/", views.measuring_day_close_view, name="day_close"), # 측정마감
    path("day_close/<str:measdate>", views.measuring_day_close_view),  # 측정마감
    path("day_reclose/<str:measdate>", views.measuring_day_reclose_view),  # 측정 재마감
    path("maps/<filename>/", views.maps_files), # 측정위치 지도맵 보여주기
]

