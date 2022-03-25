from django.urls import path
from . import views

urlpatterns = [
    path("start/", views.set_cb),
    path("stop/", views.stop_cb),
    path("msg_send/", views.msg_send),
    path("sample/", views.msg_index),
]
