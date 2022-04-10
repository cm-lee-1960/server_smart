from django.urls import path
from . import views

########################################################################################################################
# REST API 기능 제공
########################################################################################################################
app_name = 'api'
urlpatterns = [
    # path("phonegroup/list/<str:measdate>/", views.ApiPhoneGroupLV.as_view(), name='phoneGroupList'), # 단말그룹 리스트
    # path("phonegroup/list/<str:measdate>/", views.PhoneGroupAPIView.as_view(), name='phoneGroupList'), # 단말그룹 리스트
    path("phonegroup/list/<str:measdate>/", views.phonegroup_list, name='phoneGroupList'), # 단말그룹 리스트
    path("message/list/<int:phonegroup_id>/", views.message_list, name='messageList'),  # 메시지 리스트
    path("message/delete/<int:message_id>", views.ApiMessageDV.as_view(), name='messageDelete'), # 메시지 전송취소
    path("message/send/", views.sendMmessage, name='messageSend'), # 문자 메시지 전송)
    path("phonegroup/update/", views.updatePhoneGroup, name="phoneGroupUpdate") # 단말그룹 저장
]
