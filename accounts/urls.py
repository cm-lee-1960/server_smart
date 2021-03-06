from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'
urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(template_name='accounts/login_form.html'), name='login'),
    path('login/', views.login, name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGIN_URL), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    #path('home/', views.home, name='home')
    path('changepw/', views.change_password, name='changepw'), 
    path('changepwpage/', views.change_password_page, name='changepwpage'),
]

# from django.contrib import admin

# admin.site.index_template = 'admin/custom_index.html'
# admin.autodiscover()