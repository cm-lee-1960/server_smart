from datetime import datetime, timedelta
import time, requests
import telegram
from telegram.ext import CommandHandler, MessageHandler
# from telegram import ParseMode
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from . import tele_chatbot
from management.models import ChatMemberList, Center


########################################################################################################################
# 텔레그램 봇 클래스
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.03 - 텔레그램 봇 관련 함수를 클래스로 랩핑함 
# 2022.03.07 - 전송된 텔레그램 메시지를 회수 또는 재전송하는 함수를 추가함(del_message(...))
# 2022.03.13 - 텔레그램 봇 메시지 전송 제약(분당 20건)을 회피하기 위해서 5초 동안 전송된 메시지가
#              2건 이상일 경우 2초 대기
#
########################################################################################################################
class TelegramBot:
    ''' Telegram 인스턴스(메시지 전송, 챗봇활성화) '''
    def __init__(self):
        self.bot_token = settings.BOT_TOKEN
        self.bot = telegram.Bot(self.bot_token)
        self.max_length = 512  # 텔레그램 메시지로 보낼 수 있는 최대 문자길이(Bytes)
        self.port = 5000
        self.webhook_url = 'https://e5a0-121-165-124-29.ngrok.io'

        ############### 텔레그램 Limit Check 를 위한 변수(3.10)
        self.now_time = time.time()
        self.pre_time = time.time()
        self.term = 0   ## delay time
        self.count = 0  

    
    # ------------------------------------------------------------------------------------------------------------------
    # 메시지 내용(문자열)이 특정 크기 이상은 잘라낸다
    # 2022.02.27 - 메시지 내용 중에서 디버깅을 위해 관련정보를 붙이다 보니 512 bytes가 초과되어
    #              텔레그램 전송시 오류 발생
    #            - 오류메시지 (Flood control exceeded. Retry in 11.0 seconds)
    #            - https://stackoverflow.com/questions/51423139/python-telegram-bot-flood-control-exceeded
    # ------------------------------------------------------------------------------------------------------------------
    def unicode_truncate(self, s, length, encoding='utf-8'):
        """ 전송할 메시지 내용을 유니코드 기반으로 특정 길이만큼 잘라 반환하는 함수
            - 파라미터
              . s: 문자 메시지 내용
              . length: 최대 길이(문자를 자르고자 하는 최대 길이)
            - 반환값: 문자열
        """
        self.encoded = s.encode(encoding)[:length]
        return self.encoded.decode(encoding, 'ignore')

    # ------------------------------------------------------------------------------------------------------------------
    # 텔레그램 메시지를 전송한다.
    # 2022.02.27 - 텔레그램 봇에 메시지를 보낼때 제약사항이 있는 것으로 확인됨
    # My bot is hitting limits, how do I avoid this?
    # When sending messages inside a particular chat, avoid sending more than one message per second. 
    # We may allow short bursts that go over this limit, but eventually you'll begin receiving 429 errors.
    #
    # If you're sending bulk notifications to multiple users, the API will not allow more than 30 messages per second or so. 
    # Consider spreading out notifications over large intervals of 8—12 hours for best results.
    # [출처]https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
    #
    # Telegram bot API limitations
    # I have simple telegram bot with simple rate limiter:
    # it doesn't use group chats;
    # it sends only 1 message per second inside particular chat;
    # it sends less than 20 messages per minute inside particular chat;
    # But i always receive 429 error:
    # [출처] https://stackoverflow.com/questions/44152519/telegram-bot-api-limitations
    # ------------------------------------------------------------------------------------------------------------------
    def send_message_bot(self, channelId, message):
        """ 텔레그램 메시지를 전송하는 함수
            - 파라미터
              . channelId: 채널ID
              . message: 메시지 내용
            - 반환값: 없음
        """
        try:
            # 메시지를 보내기 전에 5초 동안 메시지가 2건 이상 보냈으면 2초를 대기한다. 
            # now = datetime.strptime("2022-03-11 22:30:08", "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            from_dt = now - timedelta(seconds=5)
            from monitor.models import Message
            qs = Message.objects.filter(sendTime__gte=from_dt).filter(sendTime__lte=now)
            if qs.exists() and qs.count() >= 2:
                time.sleep(2)
            
            # 메시지 앞뒤로 <code></code> 래핑을 한다. (04.26)
            # message = '<code>' + message + '</code>'

            # 메시지를 텔레그램으로 전송한다.
            sent_msg = self.bot.sendMessage(channelId, text=message, parse_mode='HTML')
            return sent_msg

        except Exception as e:
            # 에러 코드 및 내용을 반환한다.
            print("Telegram 메시지 전송 실패:"+str(e))
            raise Exception("send_message_bot(): %s" % e)

    # ------------------------------------------------------------------------------------------------------------------
    # 보낸 메시지 삭제(회수) 함수 - Chat_ID와 Message_ID 정보로 삭제 가능
    # 삭제하고자 하는 Message 에 필요한 정보를 DB에서 읽어와서 삭제
    # 2022.03.19 - 전달되는 파라미터 약어명를 내용을 알 수 있도록 풀명으로 수정함
    # ------------------------------------------------------------------------------------------------------------------
    def delete_message(self, chat_id, message_id):
        """전송된 메시지를 삭제하는 함수
            파라미터: 수신자ChatID, 보낸메시지ID
            반환값: Boolean (True / False)"""
        result = self.bot.deleteMessage(chat_id=chat_id, message_id=message_id)
        return result

    # ------------------------------------------------------------------------------------------------------------------
    # Telegram 채팅방 멤버 추방 함수
    # ------------------------------------------------------------------------------------------------------------------
    def ban_member(self, chat_id, user_id):
        '''채팅방 추방 함수
        .파라미터
         - chat_id : 추방할 채팅방ID
         - user_id : 추방할 유저ID
        .반환값: 성공 시 True '''
        try:
            result = self.bot.banChatMember(chat_id=chat_id, user_id=user_id)
        except Exception as e:
            print("텔레그램 채팅방 멤버 추방:"+str(e))
            result = False
            raise Exception("ban_member(): %s" % e)
        return result  # 성공 시 True

    # ------------------------------------------------------------------------------------------------------------------
    # Telegram Limit Check 함수
    # limit : 30메시지/1초  or  20메시지/그룹  --> 1초간 20 메시지를 Limit로 설정
    # 1초 내 시간으로 연속 20개 메시지 전송한 경우 (1초 - (현재 시간 - 직전 전송 시간))의 Delay 설정
    # ------------------------------------------------------------------------------------------------------------------
    def check_limit(self):
        self.now_time = time.time()
        self.term = self.now_time - self.pre_time
        if self.count >= 20:
            time.sleep(self.term)
            self.count = 0
        elif self.term > 1:
            self.count = 0
        else:
            self.count += 1
        self.pre_time = self.now_time



    # ------------------------------------------------------------------------------------------------------------------
    # 챗봇 활성화 : 127.0.0.1:8000/message/start 주소 진입하여 웹훅 활성화 (/message/stop : 비활성화)
    # 챗봇 함수 변경 시 웹훅 재시작 필요
    # 현재 NGROK 로 뚫은 터널 사용, 주소 변경 시 함수 내 self.webhook_url 주소 및 settings 의 ALLOWED_HOST 변경 필요
    # ------------------------------------------------------------------------------------------------------------------
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
            requests.get(f'https://api.telegram.org/bot{self.bot_token}/deleteWebhook')
            #self.updater.stop()
    

########################################################################################################################
# Telethon 클래스
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.28 - Telethon 라이브러리를 이용해 Telegram API 호출 및 채팅방 멤버 리스트 얻기
#            - 추후 Telegram Bot -> Telethon 변경 가능성 검토
########################################################################################################################
from telethon import TelegramClient
import asyncio

class RunTelethon():
    def __init__(self):
        self.api_id = settings.TELEGRAM_API_ID
        self.api_hash = settings.TELEGRAM_API_HASH
        self.token = settings.BOT_TOKEN
        self.session_file = 'smart_project_9473'

    # Telethon 연결
    def connect(self):
        self.client = TelegramClient(self.session_file, self.api_id, self.api_hash)
        self.client.start(bot_token=self.token)
        # client.run_until_disconnected()

    # Telethon 연결 해제(필수)
    def disconnect(self):
        self.client.disconnect()

    # 채팅방 멤버 리스트 얻는 함수
    async def get_chat_members(self, chat_id):
        members = await self.client.get_participants(entity=int(chat_id))
        members_list = []
        for member in members:
            user = [str(member.id), member.first_name, member.last_name, member.username, member.bot]
            members_list.append(user)
        return members_list
    
    # Telethon 연결 및 채팅방 멤버 얻은 후 연결 해제까지
    def run_get_chat_members(self, chat_id):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.connect()
        members_list = loop.run_until_complete(self.get_chat_members(chat_id))
        self.disconnect()
        return members_list
    

######################################################################################################
### 채팅방 멤버 업데이트/강퇴 함수(03.29)

def update_members(chat_id, center):
    '''특정 채팅방 멤버 업데이트 함수
        . 파라미터
         - chat_id : 채팅방ID
         - center : 해당 센터'''
    try: 
        members_list = RunTelethon().run_get_chat_members(chat_id)  # Telethon 연결하여 현재 멤버 리스트 받아오기
    except Exception as e:
        print("Telethon Run ERROR: ", str(e))
        raise Exception("update_members(): %s" % e)
    ChatMemberList.objects.filter(center=center).update(join=False)  # 해당 센터에 대한 멤버 참석여부 초기화
    for member in members_list:
        if ChatMemberList.objects.filter(userchatId = member[0], center=center):  # 기존 멤버 업데이트
            ChatMemberList.objects.filter(userchatId = member[0], center=center).update(
                chatId = chat_id,
                firstName = member[1],
                lastName = member[2],
                userName = member[3],
                isBot = member[4],
                join = True,
            )
        else:   # 신규 멤버 생성
            ChatMemberList.objects.create(
                userchatId = member[0],
                firstName = member[1],
                lastName = member[2],
                userName = member[3],
                center = center,
                chatId = chat_id,
                allowed = False,
                isBot = member[4],
                join = True,
            )
    ChatMemberList.objects.filter(center=center, allowed=False, join=False).delete()  # 미허용/미참석 상태 인원은 DB에서 삭제

def update_members_allchat():
    '''모든 채팅방에 대해 멤버 Update 진행'''
    for center in Center.objects.all():
        update_members(center.channelId, center)
    # chat_id_list = ChatMemberList.objects.values_list('chatId', 'center')  # 모든 채팅방ID-센터 추출
    # for chat_id in chat_id_list:
        # update_members(chat_id)  # 개별 채팅방 함수 반복 실행으로 모든 채팅방 업데이트

def ban_member_as_compared_db(chat_id):
    ''' 저장된 DB와 비교하여 DB에 없는 사용자 강퇴 함수(특정 채팅방)
    . 파라미터
     - chat_id : 채팅방ID
    . 반환값(dict): {유저ID : 강퇴결과}
    . 강퇴 대상 없을 경우 Null Dictionary 반환''' 
    members_list = RunTelethon().run_get_chat_members(chat_id) # Telethon 연결하여 현재 멤버 리스트 받아오기
    members_list_db = ChatMemberList.objects.filter(chatId=chat_id).values_list('userchatId', flat=True)
    result = {}  # 강퇴할 사용자와 강퇴 결과 저장을 위한 Dictionary 선언
    for member in members_list:
        if not member[0] in members_list_db:
            try:
                result_ban = TelegramBot().ban_member(chat_id, member[0])
                result.update({member[0] : result_ban})
            except Exception as e:
                print("Telegram Ban Member Error: ", str(e))
                raise Exception("ban_member_as_compared_db(): %s" % e)
    return result  # 반환값 : {채팅ID : 강퇴결과(True)} // 강퇴할 멤버 없을 경우 Null Dictionary

def ban_member_as_compared_db_allchat():
    ''' 저장된 DB와 비교하여 DB에 없는 사용자 강퇴 함수(모든 채팅방)
    . 반환값(dict): {채팅방ID : {유저ID:강퇴결과}}
    . 강퇴 대상 없을 경우 Null Dictionary 반환'''
    chat_id_list = ChatMemberList.objects.values_list('chatId', flat=True).distinct()  # 모든 채팅방ID 추출
    result = {}
    for chat_id in chat_id_list:
        result_ban = ban_member_as_compared_db(chat_id)  # 개별 채팅방 강퇴 함수 반복 실행으로 모든 채팅방 업데이트
        result.update({chat_id : result_ban})
    return result
    
def ban_member_not_allowed_all():
    ''' 사용자DB에서 allowed가 False인 유저 일괄 추방 함수(파라미터 없이 사용)
    . 반환값(dict):  {chat : 채팅방ID, 유저ID : 강퇴결과}
    . 강퇴 대상 없을 경우 Null Dictionary 반환'''
    update_members_allchat()  # 모든 채팅방에 대해 현재 멤버 업데이트
    not_allowed_members_list = ChatMemberList.objects.filter(allowed=False)  # 입장 허용안된 유저 정보 추출
    result_list = []
    try:
        for member in not_allowed_members_list:
            result_ban = TelegramBot().ban_member(member.chatId, member.userchatId)
            result_list.append(result_ban)
            #result.update({'chat' : member['chatId'], member['userchatId'] : result_ban})
            if result_ban == True:  # 강퇴 성공하면 해당 유저 정보는 DB에서 삭제
                member.delete()
                # ChatMemberList.objects.filter(userchatId=member.userchatId, chatId=member.chatId).delete()
        if False not in result_list:
            result = True
        else:
            result = False
    except Exception as e:
        result = False
        print("Telegram Ban All-Member Error: ", str(e))
        raise Exception("ban_member_not_allowed_all(): %s" % e)
    return result


def ban_member_not_allowed(center):
    ''' 사용자DB에서 allowed가 False인 유저 일괄 추방 함수(특정 센터)
    . 반환값(dict):  {result : True/False, chat : 채팅방ID, 유저ID : 강퇴결과}
    . 강퇴 대상 없을 경우 Null Dictionary 반환'''
    update_members(center.channelId, center)  # 해당 채팅방에 대해 현재 멤버 업데이트
    not_allowed_members = ChatMemberList.objects.filter(center=center, chatId=center.channelId, allowed=False)  # 입장 허용안된 유저 정보 추출
    result_list = []
    try:
        for member in not_allowed_members:
            result_ban = TelegramBot().ban_member(member.chatId, member.userchatId)
            result_list.append(result_ban)
            if result_ban == True:  # 강퇴 성공하면 해당 유저 정보는 DB에서 삭제
                member.delete()
        if False not in result_list:
            result = True
        else:
            result = False
    except Exception as e:
        result = False
        print("Telegram Ban Center-Member Error: ", str(e))
        raise Exception("ban_member_not_allowed(): %s" % e)
    return result
######################################################################################################