from django.urls import path
from . import views

urlpatterns = [
    path("report/", views.make_report),
    path("register/", views.make_register),
    path('new/', views.new, name='new'),
    path('make_register/',views.make_register,name='make_register'),
    path('make_todayregister/',views.make_todayregister,name='make_todayregister'),
    path('delete_register/',views.delete_register,name='delete_register'),
    path('delete_todayregister/',views.delete_todayregister,name='delete_todayregister'),
    path('test_layout/',views.test_layout,name='test_layout'),
]
