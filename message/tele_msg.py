import telegram
from telegram.ext import CommandHandler, MessageHandler
from django.conf import settings
from . import tele_chatbot

# bot_token = '5295955513:AAE7eyfD0xUANk-ZjKAsIhti_pXoV_eh_KM'
#webhook_url = 'https://1452-121-165-124-29.ngrok.io'

bot_token = settings.BOT_TOKEN
bot = telegram.Bot(bot_token)

#--------------------------------------------------------------------------------------------------
# 메시지 내용(문자열)이 특정 크기 이상은 잘라낸다
# 2022.02.27 - 메시지 내용 중에서 디버깅을 위해 관련정보를 붙이다 보니 512 bytes가 초과되어 텔레그램 전송시 오류 발생
#            - 오류메시지 (Flood control exceeded. Retry in 11.0 seconds)
#            - https://stackoverflow.com/questions/51423139/python-telegram-bot-flood-control-exceeded
#--------------------------------------------------------------------------------------------------
def unicode_truncate(s, length, encoding='utf-8'):
    encoded = s.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')

#--------------------------------------------------------------------------------------------------
# 텔레그램 메시지를 전송한다.
#--------------------------------------------------------------------------------------------------
def send_message_bot(channelId, message):
    bot_token = settings.BOT_TOKEN
    max_length = 512 # 텔레그램 메시지로 보낼 수 있는 최대 문자길이(Bytes)
    bot = telegram.Bot(bot_token)
    bot.sendMessage(channelId, text=unicode_truncate(message,max_length))


# 챗봇 활성화
def set_chatbot(set, webhook_url, port=5000, token=bot_token):
    updater = tele_chatbot.set_updater(token)

    # 명령어 챗봇 활성화
    updater.dispatcher.add_handler(CommandHandler('help', tele_chatbot.helps, pass_args = False))
    updater.dispatcher.add_handler(CommandHandler('when', tele_chatbot.when, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('where', tele_chatbot.where, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('search', tele_chatbot.search, pass_args=True))

    # 버튼식 챗봇 활성화
    updater.dispatcher.add_handler(tele_chatbot.tele_btn)

    # webhook 실행
    if set == 1 :

        updater.start_webhook(#listen='',
            port=port,
            webhook_url=webhook_url)
        # updater.idle()

    # webhook 종료
    elif set == 0 :
        updater.stop()