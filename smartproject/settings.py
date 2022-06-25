"""
Django settings for smartproject project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from os.path import join

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-g%+xa#(om)nj^!u!&8w7kzicx9*!#g*1-atw87f7s8@hy2h&yp'

import os, json 
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

secret_file = os.path.join(BASE_DIR, 'secrets.json')


# ----------------------------------------------------------------------------------------------------------------------
# 보안이 민감한 데이터를 파일에서 읽어와서 환경정보를 설정하는 부분
# ----------------------------------------------------------------------------------------------------------------------
with open(secret_file) as f:
	secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} enviroment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")

# 텔레그램 봇 토큰, 채널ID, 카카오 REST API키를 찾아 온다.
BOT_TOKEN = get_secret("BOT_TOKEN")
CHANNEL_ID = get_secret("CHANNEL_ID")
KAKAO_REST_API_KEY = get_secret("KAKAO_REST_API_KEY")
# Telethon(채팅방 유저 업데이트) 호출을 위한 API ID/HASH 값을 찾아 온다.
TELEGRAM_API_ID = get_secret("TELEGRAM_API_ID")
TELEGRAM_API_HASH = get_secret("TELEGRAM_API_HASH")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://nqi.kt.com']


# Application definition

INSTALLED_APPS = [
    ### django apps ####################################################################################################
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ### third apps #####################################################################################################
    'django_extensions',
    'rest_framework',
    # 'django_db_logger',
    ### local apps #####################################################################################################
    'monitor',
    'analysis',
    'message',
    'management',
    'accounts',
    'logs',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'smartproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'smartproject', 'templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'smartproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# 향후 데이터베이스 관련 중요정보는 파일을 분리해서 관리해야 함
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'smart',
        'USER': 'smartnqi',
        'PASSWORD': 'nwai1234!',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True

LANGUAGE_CODE = 'ko-kr' #국가 설정
TIME_ZONE = 'Asia/Seoul' #시간대 설정
USE_I18N = True #국제화(Internationalization)
USE_L10N = True #지역화(localization)
USE_TZ = False #장고 시간대


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'smart/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'smartproject', 'static')
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# 미디어  경로 지정 일일보고 파일 저장 및 다운을 위한 설정
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 로그 관련 설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'logs.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG'
        },
        'django.request': { # logging 500 errors to database
            'handlers': ['db_log'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}

# 관리자 페이지 앱들 정렬 순서
APPS_ORDERING = {
    "측정 모니터링": 1,
    # "전송 메시지": 2,
    "분석 및 보고": 3,
    "환경설정 관리": 4,
    "인증 및 권한": 5,
    "디버깅 로그": 6,
}

# 환경설정 관리 앱의 모델들 정렬 순서
MANAGEMENT_MODELS_ORDERING = {
    "금일 측정조": 1,
    "측정단말 사전정보": 2,
    "모풀로지 맵": 3,
    "속도저하 기준": 4,
    "전송실패 기준": 5,
    "측정 보고주기": 6,
    "모풀로지": 7,
    "모폴로지 상세": 8,
    "센터정보": 9,
    "센터별 관할구역": 10,
    "채팅방 멤버 리스트": 11,
    "메시지 자동전송 설정": 12,
    "기타 환경설정": 13,
}

LOGIN_REDIRECT_URL = 'http://localhost:8000/'
LOGOUT_REDIRECT_URL = '/'

SCHEDULER_DEFAULT = True

SESSION_COOKIE_AGE = 86400 # 세션타임(하루)
SESSION_SAVE_EVERY_REQUEST = True