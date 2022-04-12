from django.apps import AppConfig

########################################################################################################################
# 디버깅 로그 관리자 앱
# [사용법] https://pypi.org/project/django-db-logger/
# 1. install
#   > pip install django-db-logger
#
# 2. Add “django_db_logger” to your INSTALLED_APPS setting
#   INSTALLED_APPS = {
#        ...
#       'django_db_logger',
#   }
#
# 3. Add handler and logger to LOGGING setting
#   LOGGING = {
#       'version': 1,
#       'disable_existing_loggers': False,
#       'formatters': {
#           'verbose': {
#           'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#        },
#   .....
#
# 4. Run python manage.py migrate to create django-db-logger models
# > python manage.py makemigrations logs
# > python manage.py migrate logs
#
# 5. Use django-db-logger like
#   import logging
#   db_logger = logging.getLogger('db')
#
#   db_logger.info('info message')
#   db_logger.warning('warning message')
#   db_logger.error('error message')
#
#   try:
#       1/0
#   except Exception as e:
#       db_logger.exception(e)
# ----------------------------------------------------------------------------------------------------------------------
# 2022.04.02 - 디버그 로그 관리앱에 대한 사용법 및 주석 추가
#
########################################################################################################################

class LogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logs'
    verbose_name = "디버깅 로그"
