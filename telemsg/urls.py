from django.urls import path
from . import views

urlpatterns = [
    path("start/", views.set_cb),
    path("stop/", views.stop_cb)
]
