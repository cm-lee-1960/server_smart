from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tele_msg import TelegramBot
from .xmcs_msg import send_sms, send_sms_queryset
from monitor.models import Message
from rest_framework.parsers import JSONParser
import requests

# Create your views here.

# ngrok_url = 'https://1069-121-165-124-29.ngrok.io'

# 인스턴스 선언
bot = TelegramBot()


# 텔레그램 웹훅 활성화 (주소:/message/telegram/bot_start)
def set_cb(request):
    bot.set_chatbot(1)
    return HttpResponse("Chatbot 설정 완료")

# 텔레그램 웹훅 비활성화 (주소:/message/telegram/bot_stop)
def stop_cb(request):
    bot.set_chatbot(0)
    return HttpResponse("Chatbot 종료 완료")

####################################### 서버 연결 후 작성 예정 #######################################
# 텔레그램 채팅방에 신규 멤버 입장 시 (주소:/message/telegram/)
# 웹훅 활성화 후 동작 가능
# def listen_webhook(request):
#     if request.method != 'POST':
#         return HttpResponse("Error")
#     data = JSONParser().parse(request)
#     try:
#         if data['message']['new_chat_participant'].exists():
#             data['message']['new_chat_participant']['id']
#             data['message']['new_chat_participant']['first_name']
####################################################################################################