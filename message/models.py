from xml.dom.pulldom import PROCESSING_INSTRUCTION
from django.db import models

###################################################################################################
# 전송된 텔레그램 메시지 클래스
# -------------------------------------------------------------------------------------------------
# 2022.03.07 - Chat ID와 Message ID로 전송된 메시지를 삭제 가능함
###################################################################################################
class SentTelegramMessage(models.Model):
  """ 전송된 텔레그램 메시지 정보 """
 
  chat_id = models.CharField(max_length=20, null=True, blank=True, verbose_name='Chat ID')  ## chat id는 admin page 미노출
  chat_type = models.CharField(max_length=10, null=True, blank=True, verbose_name='Type')
  chat_title = models.CharField(max_length=100, null=True, blank=True, verbose_name='Chat Title')
  chat_message_id = models.BigIntegerField(null=True, blank=True, verbose_name='Message ID')
  chat_date = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name='날짜')  ## 전송 메시지 시각이 <UTC> 기준이라 auto_now_add 적용
  chat_text = models.TextField(null=True, blank=True, verbose_name='내용')
  is_del = models.BooleanField(default=False, verbose_name='회수여부')
  #is_resend = models.BooleanField(default=False, verbose_name='재전송여부')

  class Meta:
    verbose_name = "텔레그램 메시지"
    verbose_name_plural = "텔레그램 메시지"


class SentXroshotMessage(models.Model):
  """ 크로샷으로 보낼 SMS 메시지 """
  message = models.TextField(null=True, blank=True, verbose_name="내용")
  receiver = models.TextField(null=False, blank=False, verbose_name="번호")
  send_date = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name='송신시간')
  result = models.CharField(max_length=10, null=True, blank=True, verbose_name="결과")