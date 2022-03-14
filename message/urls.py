from django.urls import path
from . import views

urlpatterns = [
    path("start/", views.set_cb),
    path("stop/", views.stop_cb),
    path("xroshot_send/", views.xroshot_send),
    path("xroshot/", views.xroshot_index),
]
