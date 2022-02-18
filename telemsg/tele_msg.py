import telegram
from telegram.ext import CommandHandler, MessageHandler
from . import tele_chatbot

bot_token = '5295955513:AAE7eyfD0xUANk-ZjKAsIhti_pXoV_eh_KM'
#webhook_url = 'https://1452-121-165-124-29.ngrok.io'

# bot 설정
bot = telegram.Bot(bot_token)
mc = '-736183270' 

# 단순 메시지 전송
def send_message_bot(sender, **kwargs):
# def send_message(chat_id, msg):
    # bot.send_message(chat_id=mc, text=msg)
    bot.sendMessage(mc, text=kwargs['instance'].message)


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