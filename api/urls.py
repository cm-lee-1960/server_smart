from django.urls import path
from . import views

########################################################################################################################
# REST API 기능 제공
########################################################################################################################
app_name = 'api'
urlpatterns = [
    path("phonegroup/list/<str:measdate>/", views.ApiPhoneGroupLV.as_view(), name='phoneGroupList'), # 단말그룹 리스트
    path("message/list/<int:phonegroup_id>/", views.ApiMessageLV.as_view(), name='messageList'),  # 메시지 리스트
]
