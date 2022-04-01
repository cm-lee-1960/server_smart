from __future__ import unicode_literals
import logging
from django.contrib import admin
from django.utils.html import format_html
from .models import StatusLog

DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE = 10

########################################################################################################################
# 디버깅 로그 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
########################################################################################################################
class StatusLogAdmin(admin.ModelAdmin):
    """어드민 페이지에 디버깅 로그 정보를 보여주기 위한 클래스"""
    list_display = ('level', 'colored_msg', 'traceback', 'create_datetime_format')
    list_display_links = ('colored_msg', )
    list_filter = ('level', )
    list_per_page = DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE

    # 로그 수준에 따라서 색상을 표현한다.
    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = 'green'
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg)
    colored_msg.short_description = '로그내용'

    def traceback(self, instance):
        return format_html('<pre><code>{content}</code></pre>', content=instance.trace if instance.trace else '')
    traceback.short_description = '추적내용'

    # 디버깅 로그의 생성일자에 대한 날짜 포맷을 설정한다.
    def create_datetime_format(self, instance):
        return instance.create_datetime.strftime('%Y-%m-%d %X')
    create_datetime_format.short_description = 'Created at'

# 관리자 페이지에 모델을 등록한다.
admin.site.register(StatusLog, StatusLogAdmin)