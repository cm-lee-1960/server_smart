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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from analysis.views import dashboard

########################################################################################################################
# 스마트상황실 프로젝트
# ----------------------------------------------------------------------------------------------------------------------
# smart_project
#   ├- accounts : 로그인 관련 모듈
#   ├- analysis : 분석 관련 모듈 (홈 데시보드 및 일일보고)
#   |      ├- migrations : 데이터베이스 관련 파일
#   |      ├- static : 정적파일
#   |      └- templates
#   |            └- analysis : 화면
#   |
#   ├- management : 운영환경 관리 관련 모듈
#   ├- message : 전송 메시지 관련 모듈
#   ├- monitor : 측정 모니터링 관련 모듈
#   ├- scheduler : 백그라운드 스케쥴 작업 관련 모듈
#   ├- smartproject : 스마트상황실 프로젝트 메인 디렉토리
#   |      ├- static
#   |      └- templates
#   |            └- admin : 커스터마이징 관리자 페이지
#   └- staticfiles : STATIC 파일
#
########################################################################################################################

urlpatterns = [
    path('', dashboard),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("monitor/", include("monitor.urls")), # 측정 모니터링
    path("analysis/", include("analysis.urls")), # 분석
    path("message/", include("message.urls")), # 전송 메시지
    path("accounts/", include("accounts.urls")), # 계정
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # STATIC 파일
urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT) # MEDIA 파일

# 어드민 페이지 변경
admin.site.index_title = "스마트 상황실"
admin.site.site_header = "스마트 상황실 관리"
admin.site.site_title = "스마트 상황실"
