from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tele_msg import TelegramBot
from .models import SentXroshotMessage
from .forms import SentXroshotMessageForm
from .xmcs_msg import send_sms
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


# 크로샷 메시지 작성 페이지 (임시)  // (3.13)
def msg_index(request):
    if request.method=='POST':
        message = {'message_all':Message.objects.all(), 'message':request.POST['selected_message'], \
                    'sendType':request.POST['sendType'], 'channelId':request.POST['channelId']}
        return render(request, 'message/xroshot_page.html', message)
    else:
        message = {'message_all':Message.objects.all()}
        return render(request, 'message/xroshot_page.html', message)


# 작성한 메시지를 바탕으로 메시지 전송  //  (3.13)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def msg_send(request):
    if request.method=='POST':
        if request.POST['sendType'] == 'XMCS':
            form = SentXroshotMessageForm(request.POST)
            if form.is_valid():
                #messages = form.save(commit=False)
                form.save()
                result = send_sms()
                if 'Result: 10000' in result:
                    return HttpResponse(result+'\nSuccess!')
                else:
                    return HttpResponse(result+'\nFailed..')
            else:
                return HttpResponse("Error occured. Please check your message or phone-number.")
        elif request.POST['sendType'] == 'TELE':
            try:
                if request.POST['resend'] == 'True':
                    result = '\nSended'
                elif request.POST['retreive'] == 'True':
                    result = bot.delete_message(sentMessage.chat_id, sentMessage.chat_message_id)
                return HttpResponse(result)
            except Exception as e:
                raise Exception("telegram message send error: %s" % e) 
    
    else:
        print("잘못된 요청입니다.")
        return HttpResponse("Bad Request..")
