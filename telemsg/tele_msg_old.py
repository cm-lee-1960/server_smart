#봇정보 관리 방법 구현
import telegram

#메세지 함수
def send_message_bot(sender, **kwargs):
    print("### 텔레그램 함수 호출")
    #message = message
    #send_message = "텍스트는" + message.number + "더하기" + message.boot + "더하기" +  message.address
    # token = '5131482190:AAEY7A07dWeqWaIjZZGDiVjoZ50kMKdcayM'
    token = '5041688809:AAFuRPnLZxbVY3014X4ElolaH564Mm9CiYI'
    bot = telegram.Bot(token)
    print("good luck")
    #bot.message_loop(start_telegram)
    # chat_id = '1047352647'
    mc = '-736183270' 
    bot.sendMessage(mc, text=kwargs['instance'].message)