from django.urls import path
from . import views

urlpatterns = [
    path("report/", views.make_report),
    path("register/", views.make_register),
    path('new/', views.new, name='new'),
    path('make_register/',views.make_register,name='make_register'),
]
