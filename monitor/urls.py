from django.urls import path
from . import views

urlpatterns = [
    path("json/", views.receive_json), # 측정 데이터 처리
    path("maps/<filename>/", views.maps_files), # 측정위치 지도맵 보여주기

]
