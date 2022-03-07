from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from django import forms
from .models import SentTelegramMessage
from django.utils.html import format_html
import requests
from django.conf import settings
from .tele_msg import TelegramBot


class SentTelegramMessageAdmin(admin.ModelAdmin):
    '''어드민 페이지에 보낸 메시지 정보를 보여주기 위한 클래스'''

    list_display = ['chat_type', 'chat_title', 'chat_message_id', 'chat_date', 'chat_text', 'is_del',]
    list_display_links = ['chat_text']
    search_fields = ('chat_type', 'chat_title', 'chat_date', 'chat_text', )
    list_filter = ['is_del',]
    actions = ['del_message_action', 'resend_message_action']

    ########### Admin Page에서 메시지 회수 액션 제공 (3.7) #############
    def del_message_action(self, request, queryset):
      bot = TelegramBot()
      del_list = queryset.values_list('id', 'chat_id', 'chat_message_id')
      for id in del_list:
        result = bot.del_message(id[1], id[2])
        if result.ok:
          queryset.filter(id=id[0]).update(is_del=True)
        else:
          print("회수 실패 - 메시지 선택을 확인하여주세요.")
          raise Exception("회수 실패 - 메시지 선택을 확인해주세요. \n 이미 회수된 메시지가 선택되어 있을 수 있습니다.")
    del_message_action.short_description = '선택한 메시지 회수'

    ########### Admin Page에서 메시지 재전송 액션 제공 (3.7) #############
    def resend_message_action(self, request, queryset):
      bot = TelegramBot()
      res_list = queryset.values_list('chat_id', 'chat_text')
      for id in res_list:
        bot.send_message_bot(id[0], id[1])
    resend_message_action.short_description = '선택한 메시지 재전송'



admin.site.register(SentTelegramMessage, SentTelegramMessageAdmin)