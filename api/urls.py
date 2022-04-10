from django.urls import path
from . import views

########################################################################################################################
# REST API 기능 제공
########################################################################################################################
app_name = 'api'
urlpatterns = [
    path("phonegroup/list/<str:measdate>/", views.phonegroup_list, name='phoneGroupList'), # 단말그룹 리스트
    path("message/list/<int:phonegroup_id>/", views.message_list, name='messageList'),  # 메시지 리스트
    path("message/delete/<int:message_id>", views.delete_message, name='messageDelete'), # 텔레그램 메시지 전송취소
    path("message/send/", views.send_message, name='messageSend'), # 문자 메시지 전송)
    path("phonegroup/update/", views.update_phonegroup, name="phoneGroupUpdate") # 단말그룹 측정조 변경
]
