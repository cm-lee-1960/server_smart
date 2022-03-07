from django.apps import AppConfig


class TelemsgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message'
    verbose_name = "전송 메시지"