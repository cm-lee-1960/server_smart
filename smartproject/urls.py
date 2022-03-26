"""smartproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from analysis.views import dashboard

urlpatterns = [
    path('', dashboard),
    # path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("monitor/", include("monitor.urls")), # 측정 모니터링
    path("analysis/", include("analysis.urls")), # 분석
    path("message/", include("message.urls")), # 전송 메시지
    path("accounts/", include("accounts.urls")), # 계정
]

# 어드민 페이지 변경
admin.site.index_title = "스마트 상황실"
admin.site.site_header = "스마트 상황실 관리"
admin.site.site_title = "스마트 상황실"
