from django.urls import path
from . import views

########################################################################################################################
# REST API 기능 제공
#
#  데시보드 화면(dashboard_form.html)
#  ┌-----------------------------------------┐
#  | ┌------------┐ ┌------------┐           |         시점: created, time interfal
#  | | 오늘의측정 | | 센터별현황 |<----------╂----┰--- phonegroup/list/<str:measdate>/
#  | |            | |            |           |    |    시점: 버튼 클릭시
#  | └------------┘ └------------┘  종료/마감|<---|--- end/<int:phonegroup_id>/   <-- API 모듈로 랩핑할지 고민
#  | ┌-------------------------------------┐ |    |    day_close/<str:measdate>/
#  | | 단말그룹 현황                       |<╂----┘
#  | |                                     | |
#  | └-------------------------------------┘ |
#  | ┌-----------------┐ ┌-----------------┐ |         시점: 단말그룹 선택(클릭)시
#  | |이벤트/문자/텔레 | | 메시지상세내용  |<╂-------- message/list/<int:phonegroup_id>/
#  | |                 | |                 | |         시점: 버튼 클릭시
#  | |                 | |     전송/회수<--╂-╂-------- message/send/
#  | └-----------------┘ └-----------------┘ |         message/delete/<int:message_id>/
#  └-----------------------------------------┘
# ----------------------------------------------------------------------------------------------------------------------
# 2022.05.02 - 주석 추가
#
########################################################################################################################
app_name = 'api'
urlpatterns = [
    path("phonegroup/list/<str:measdate>/", views.phonegroup_list, name='phoneGroupList'), # 단말그룹 리스트
    path("phonegroup/update/centerANDmorphology/", views.centerANDmorphology_list, name='centerANDmorphologyList'),  # 센터 및 모폴로지 리스트
    path("phonegroup/update/info/", views.update_phonegroup_info, name="PhoneGroupUpdate"),  # 단말그룹 정보 변경
    path("message/list/<int:phonegroup_id>/", views.message_list, name='messageList'),  # 메시지 리스트
    path("message/delete/<int:message_id>/", views.delete_message, name='messageDelete'), # 텔레그램 메시지 전송취소
    path("message/send/", views.send_message, name='messageSend'), # 문자 메시지 전송
    path("message/new/", views.new_msg_render, name='newMessageHTML'), # 새 메시지 창
    path("message/new/send/", views.send_new_msg, name='newMessageSend'), # 새 메시지 전송
    path("message/get_chatmembers/<str:centerName>/", views.get_chatmembers, name='getChatMembers'),  # 채팅방 멤버 리스트
    path("message/ban_chatmember/<int:member_id>/", views.ban_chatmember, name='banChatMember'),  # 개별 인원 강퇴
    path("message/ban_chatmember/center/<str:centerName>/", views.ban_center_chatmembers, name='banCenterChatMembers'),  # 센터 전체 강퇴
    path('monitor/makemap/<int:phonegroup_id>/', views.make_map, name='makemap'), # 측정데이터 지도맵
    path('monitor/monitoringCondition/', views.monitoring_condition, name='monitoringCondition'), # 측정 시작/종료
    path('monitor/checkdata/<int:phonegroup_id>/', views.check_data, name='checkdata'),  # 데이터 상세보기
    path('monitor/checkdata/<int:phonegroup_id>/checkmessage/', views.check_message, name='checkmessage'),  # 종료 메시지 보기(간이)
    path('phonegroup/unmanage/<int:phonegroup_id>/', views.unmanage_pg, name='unmanage_pg'),  # managa=False 만들기
    path('phonegroup/autosend/<int:phonegroup_id>/<str:onoff>/', views.set_autosend, name='set_autosend'),  # 단말 그룹 별 자동전송 onoff 설정
]
