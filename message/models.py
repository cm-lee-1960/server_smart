from xml.dom.pulldom import PROCESSING_INSTRUCTION
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
#from .geo import KakaoLocalAPI
#from message.tele_msg import TelegramBot # 텔레그램 메시지 전송 클래스
#from message.xmcs_msg import send_sms # 2022.03.04 크로샷 메시지 전송 함수 호출
#from management.models import Morphology, MorphologyMap

######################## 텔레그램 전송된 메시지 DB 저장 - 삭제 기능 및 고도화 때 필요 (3.7) ########################
##### Chat ID와 Message ID 정보로 보낸 메시지 삭제 가능 
class SentTelegramMessage(models.Model):
  """ 전송된 텔레그램 메시지 정보 """
 
  chat_id = models.CharField(max_length=20, null=True, blank=True, verbose_name='Chat ID')  ## chat id는 admin page 미노출
  chat_type = models.CharField(max_length=10, null=True, blank=True, verbose_name='Type')
  chat_title = models.CharField(max_length=100, null=True, blank=True, verbose_name='Chat Title')
  chat_message_id = models.BigIntegerField(null=True, blank=True, verbose_name='Message ID')
  chat_date = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name='날짜')  ## 전송 메시지 시각이 <UTC> 기준이라 auto_now_add 적용
  chat_text = models.CharField(max_length=1000, null=True, blank=True, verbose_name='내용')
  is_del = models.BooleanField(default=False, verbose_name='회수여부')
  #is_resend = models.BooleanField(default=False, verbose_name='재전송여부')

  class Meta:
    verbose_name = "전송된 텔레그램 메시지"
    verbose_name_plural = "전송된 텔레그램 메시지"