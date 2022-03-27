from django.apps import AppConfig
from django.conf import settings

class MonitorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitor'
    verbose_name = "측정 모니터링"

    # 측정 모니터링앱 시작할 때 스케쥴러를 구동한다.
    def ready(self ):
        if settings.SCHEDULER_DEFAULT:
            import scheduler
            scheduler.start()