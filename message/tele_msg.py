import telegram
from telegram.ext import CommandHandler, MessageHandler
from telegram import ParseMode
from django.conf import settings
from . import tele_chatbot


class tele_msg:
    def __init__(self):
        self.bot_token = settings.BOT_TOKEN
        self.bot = telegram.Bot(self.bot_token)
        self.max_length = 512  # 텔레그램 메시지로 보낼 수 있는 최대 문자길이(Bytes)
        self.port = 5000
        self.webhook_url = 'https://9c70-121-165-124-29.ngrok.io'

    
# #--------------------------------------------------------------------------------------------------
# # 메시지 내용(문자열)이 특정 크기 이상은 잘라낸다
# # 2022.02.27 - 메시지 내용 중에서 디버깅을 위해 관련정보를 붙이다 보니 512 bytes가 초과되어 텔레그램 전송시 오류 발생
# #            - 오류메시지 (Flood control exceeded. Retry in 11.0 seconds)
# #            - https://stackoverflow.com/questions/51423139/python-telegram-bot-flood-control-exceeded
# #--------------------------------------------------------------------------------------------------
    def unicode_truncate(self, s, length, encoding='utf-8'):
        self.encoded = s.encode(encoding)[:length]
        return self.encoded.decode(encoding, 'ignore')
    

# # 텔레그램 메시지를 전송한다.
# # 2022.02.27 - 텔레그램 봇에 메시지를 보낼때 제약사항이 있는 것으로 확인됨
# # My bot is hitting limits, how do I avoid this?
# # When sending messages inside a particular chat, avoid sending more than one message per second. 
# # We may allow short bursts that go over this limit, but eventually you'll begin receiving 429 errors.
# #
# # If you're sending bulk notifications to multiple users, the API will not allow more than 30 messages per second or so. 
# # Consider spreading out notifications over large intervals of 8—12 hours for best results.
# # [출처]https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
# #
# # Telegram bot API limitations
# # I have simple telegram bot with simple rate limiter:
# # it doesn't use group chats;
# # it sends only 1 message per second inside particular chat;
# # it sends less than 20 messages per minute inside particular chat;
# # But i always receive 429 error:
# # [출처] https://stackoverflow.com/questions/44152519/telegram-bot-api-limitations
# #--------------------------------------------------------------------------------------------------
    def send_message_bot(self, channelId, message):
        try: 
            self.bot.sendMessage(channelId, text=self.unicode_truncate(message,self.max_length), parse_mode='HTML')
        except Exception as e:  
            print("low_throughput_check():"+str(e))
            print(message)
            raise Exception("send_message_bot(): %s" % e)


# #--------------------------------------------------------------------------------------------------
# # 챗봇 활성화 : 127.0.0.1:8000/message/start 주소 진입하여 웹훅 활성화 (/message/stop : 비활성화)
# # 챗봇 함수 변경 시 웹훅 재시작 필요
# # 현재 NGROK 로 뚫은 터널 사용, 주소 변경 시 함수 내 self.webhook_url 주소 및 settings 의 ALLOWED_HOST 변경 필요
# #--------------------------------------------------------------------------------------------------
    def set_chatbot(self, set):
        self.updater = tele_chatbot.set_updater(self.bot_token)

        # 명령어 챗봇 활성화
        self.updater.dispatcher.add_handler(CommandHandler('help', tele_chatbot.helps, pass_args = False))
        self.updater.dispatcher.add_handler(CommandHandler('when', tele_chatbot.when, pass_args=True))
        self.updater.dispatcher.add_handler(CommandHandler('where', tele_chatbot.where, pass_args=True))
        self.updater.dispatcher.add_handler(CommandHandler('search', tele_chatbot.search, pass_args=True))

        # 버튼식 챗봇 활성화
        self.updater.dispatcher.add_handler(tele_chatbot.tele_btn)

        # webhook 실행
        if set == 1 :

            self.updater.start_webhook(#listen='',
                port=self.port,
                webhook_url=self.webhook_url)
            # updater.idle()

        # webhook 종료
        elif set == 0 :
            self.updater.stop()