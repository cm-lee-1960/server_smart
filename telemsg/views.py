from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import telegram
from . import tele_msg

# Create your views here.

ngrok_url = 'https://1069-121-165-124-29.ngrok.io'

def set_cb(request):
    tele_msg.set_chatbot(1, ngrok_url)
    return HttpResponse("Chatbot 설정 완료")

def stop_cb(request):
    tele_msg.set_chatbot(0, ngrok_url)
    return HttpResponse("Chatbot 종료 완료")