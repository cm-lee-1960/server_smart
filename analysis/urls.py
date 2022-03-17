from django.urls import path
from . import views

app_name = 'analysis'
urlpatterns = [
    path("report/", views.make_report, name='report'),
    path("register/", views.make_register),
    path('new/', views.new, name='new'),
    path('make_register/',views.make_register,name='make_register'),
    path('make_todayregister/',views.make_todayregister,name='make_todayregister'),
    path('delete_register/',views.delete_register,name='delete_register'),
    path('delete_todayregister/',views.delete_todayregister,name='delete_todayregister'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('make_report/',views.make_report, name='make_report'),
]
