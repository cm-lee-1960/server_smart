from django.urls import path
from . import views

urlpatterns = [
    path("telegram/bot_start/", views.set_cb),
    path("telegram/bot_stop/", views.stop_cb),
    # path("telegram/", views.listen_webhook)  // 추후 작성 예정(서버 연결 후)
]
