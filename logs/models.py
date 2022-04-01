import logging
from django.db import models
from six import python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _

########################################################################################################################
# 디버깅 로그 관리 클래스
# ----------------------------------------------------------------------------------------------------------------------
########################################################################################################################
LOG_LEVELS = (
    (logging.NOTSET, _('NotSet')),
    (logging.INFO, _('Info')),
    (logging.WARNING, _('Warning')),
    (logging.DEBUG, _('Debug')),
    (logging.ERROR, _('Error')),
    (logging.FATAL, _('Fatal')),
)

@python_2_unicode_compatible
class StatusLog(models.Model):
    logger_name = models.CharField(max_length=100, verbose_name="로그명") # 로그명
    level = models.PositiveSmallIntegerField(choices=LOG_LEVELS, default=logging.ERROR, \
                                             db_index=True, verbose_name="로그레벨") # 로그레벨
    msg = models.TextField(verbose_name="로그내용") # 로그내용
    trace = models.TextField(blank=True, null=True, verbose_name="추적내용") # 추적내용
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='발생일시') # 발생일시

    def __str__(self):
        return self.msg

    class Meta:
        ordering = ('-create_datetime',)
        verbose_name_plural = verbose_name = '로그내역'
