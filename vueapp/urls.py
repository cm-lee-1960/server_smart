from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardVue.as_view()),
]