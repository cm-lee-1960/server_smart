from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path("phonegroup/list/<str:measdate>/", views.ApiPhoneGroupLV.as_view(), name='phoneGroupList'), # 단말그룹 리스트
]
