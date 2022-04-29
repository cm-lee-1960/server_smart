from django.urls import path
from . import views

########################################################################################################################
# REST API 기능 제공
########################################################################################################################
app_name = 'api'
urlpatterns = [
    path("phonegroup/list/<str:measdate>/", views.phonegroup_list, name='phoneGroupList'), # 단말그룹 리스트
    path("phonegroup/update/centerANDmorphology/", views.centerANDmorphology_list, name='centerANDmorphologyList'),  # 센터 및 모폴로지 리스트
    path("phonegroup/update/info", views.update_phonegroup_info, name="PhoneGroupUpdate"),  # 단말그룹 정보 변경
    path("message/list/<int:phonegroup_id>/", views.message_list, name='messageList'),  # 메시지 리스트
    path("message/delete/<int:message_id>", views.delete_message, name='messageDelete'), # 텔레그램 메시지 전송취소
    path("message/send/", views.send_message, name='messageSend'), # 문자 메시지 전송
    path("message/get_chatmembers/<str:centerName>", views.get_chatmembers, name='getChatMembers'),  # 채팅방 멤버 리스트
]
