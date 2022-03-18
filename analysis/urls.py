from django.urls import path
from . import views

app_name = 'analysis'
urlpatterns = [
    
    path("report/", views.make_report, name='report'),
    path('new/', views.new, name='new'),
    path('make_register/',views.make_register,name='make_register'),
    path('make_todayregister/',views.make_todayregister,name='make_todayregister'),
    path('make_reportmsg/',views.make_reportmsg,name='make_reportmsg'),
    path('delete_register/',views.delete_register,name='delete_register'),
    path('delete_todayregister/',views.delete_todayregister,name='delete_todayregister'),
    path('delete_reportmsg/',views.delete_reportmsg,name='delete_reportmsg'),
    path('dashboard_form/',views.dashboard_form,name='dashboard_form'),
    path('make_measlastyear5G/',views.make_measlastyear5G,name='make_measlastyear5G'),
    path('make_measlastyearLTE/',views.make_measlastyearLTE,name='make_measlastyearLTE'),
    path('delete_measlastyear5G/',views.delete_measlastyear5G,name='delete_measlastyear5G'),
    path('delete_measlastyearLTE/',views.delete_measlastyearLTE,name='delete_measlastyearLTE'),
    
    
]
