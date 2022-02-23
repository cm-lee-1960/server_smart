from django.db.models.signals import post_save
from django.db import models
from monitor.models import Phone
# from .msg import send_message

###################################################################################################
# 전송 메시지
###################################################################################################
class Message(models.Model):
    '''전송 메시지'''
    phone = models.ForeignKey(Phone, on_delete=models.DO_NOTHING)
    send_type = models.CharField(max_length=10) # 메시지유형(TELE: 텔레그램, XROS: 크로샷)
    currentCount = models.IntegerField()
    message = models.TextField()
    channelId = models.CharField(max_length=25)
    sended = models.BooleanField()
    # 전송일시 항목추가

def send_message(sender, **kwargs):
    #     bot.sendMessage(kwargs['instance'].channelId, text=kwargs['instance'].message)
    # 텔레그램 있때는 텔레그램 함수 호출하고, 정상이면 sended = True
    # 크로샷때는 어떻게 할 것인지 고민 필요
    pass

# -------------------------------------------------------------------------------------------------
# 전송 메시지가 저장된 후 텔래그램 전송 모듈을 호출한다. 
#--------------------------------------------------------------------------------------------------
post_save.connect(send_message, sender=Message)
