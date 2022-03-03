from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import telegram
from .tele_msg import tele_msg

# Create your views here.

# ngrok_url = 'https://1069-121-165-124-29.ngrok.io'

# 인스턴스 선언
tele = tele_msg()


# 텔레그램 웹훅 활성화 (주소:/message/start)
def set_cb(request):
    tele.set_chatbot(1)
    return HttpResponse("Chatbot 설정 완료")

# 텔레그램 웹훅 비활성화 (주소:/message/stop)
def stop_cb(request):
    tele.set_chatbot(0)
    return HttpResponse("Chatbot 종료 완료")