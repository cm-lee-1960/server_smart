import os
import fnmatch
import glob
from telegram.ext import Updater, Filters, ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def set_updater(bot_token):
    updater = Updater(bot_token)
    return updater

## 버튼식 기능 (~115줄)
def select_s(update, context):
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('5G', callback_data='5G'),
        InlineKeyboardButton('LTE', callback_data='LTE')],
        [InlineKeyboardButton('3G', callback_data='3G'),
        InlineKeyboardButton('WiFi', callback_data='WiFi')]])
    context.bot.send_message(chat_id=update.message.chat_id, text='조회할 서비스를 선택하세요.', reply_markup=reply_markup)
    return 'step2'


def select_y(update, context):
    query = update.callback_query  # query.data : 이전 함수에서 정의된 callback_data
    chat_id = query.message.chat_id

    # 선택한 서비스의 이름을 가진 파일을 검색하여 년도만 추출
    select_year_list = list()
    for filename in glob.glob('message/smartchoice/*' + query.data + '*'):
        filename = filename.split('_')
        select_year_list.append(filename[1])
    select_year_list = list(set(select_year_list))  # 중복제거

    # 추출한 년도로 새로운 버튼 리스트 생성
    button_length = len(select_year_list)
    if button_length == 0:
        context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text='선택하신 서비스에 대한 통계가 존재하지 않습니다.')
        return ConversationHandler.END
    else:
        select_year_rm_list = list()
        for i in range(button_length):
            select_year_rm = [InlineKeyboardButton(select_year_list[i],
                                                   callback_data=select_year_list[i] + '_' + query.data + '.png')]
            select_year_rm_list.append(select_year_rm)

        context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text='조회하실 년도를 선택하세요.')
        reply_markup = InlineKeyboardMarkup(select_year_rm_list)
        context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=reply_markup)
        return 'step3'


def select_city3(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id

    # 선택한 년도의 이름을 가진 파일을 검색하여 행정동 추출
    select_city3_list = list()
    for filename in glob.glob('message/smartchoice/*' + query.data + '*'):
        filename = filename.split('_')[0][20:]
        select_city3_list.append(filename)
    select_city3_list = list(set(select_city3_list))  # 중복제거

    # 추출한 행정동으로 새로운 버튼 리스트 생성
    button_length = len(select_city3_list)
    select_city3_rm_list = list()
    for i in range(button_length):
        select_city3_rm = [
            InlineKeyboardButton(select_city3_list[i], callback_data=select_city3_list[i] + '_' + query.data)]
        select_city3_rm_list.append(select_city3_rm)

    context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text='조회하실 행정동을 선택하세요.')
    reply_markup = InlineKeyboardMarkup(select_city3_rm_list)
    context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=reply_markup)
    return 'step4'


def send_result(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    result_filename = 'message/smartchoice/' + query.data

    try:
        context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text='조회결과는 다음과 같습니다.')
        context.bot.send_photo(chat_id=chat_id, photo=open(result_filename, 'rb'))
    except:
        context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id,
                              text='조회결과 파일에 오류가 있습니다. 관리자에게 문의해주세요.')
    return ConversationHandler.END


tele_btn = ConversationHandler(entry_points=[CommandHandler('inquiry', select_s)],
                               states={'step2': [CallbackQueryHandler(select_y)],
                                       'step3': [CallbackQueryHandler(select_city3)],
                                       'step4': [CallbackQueryHandler(send_result)]},
                                       fallbacks=[CommandHandler('inquiry', select_s)], per_message=False)



def search(update, context):
    if len(context.args) == 2:
        search_name = context.args[0]
        search_year = context.args[1]
        search_file = 'message/smartchoice/' + str(search_name) + '_' + str(search_year) + '_5G.png'
        if os.path.isfile(search_file):
            output_message = str(context.args[0]) + ' ' + str(context.args[1]) + '년 ' + '측정 결과 입니다.'
            update.message.reply_text(output_message)
            update.message.reply_photo(photo=open(search_file, 'rb'))
        else:
            output_message = '해당 행정동은 해당 년도 측정 이력이 없습니다!'
            update.message.reply_text(output_message)
    else:
        output_message = '잘못된 입력입니다. "/search 동 년도" 순으로 입력해주세요.\n * 동이름은 ~동, 년도는 4자리 숫자, 띄어쓰기 필수\n예)/search 청담동 2020'
        update.message.reply_text(output_message)


def where(update, context):
    if len(context.args) != 1:
        update.message.reply_text('잘못된 입력입니다.\n/where 년도(4자리 숫자) 로 입력해주세요.\n예)/where 2020')
    elif context.args[0].isnumeric():
        where_list = list()
        for filename in os.listdir('message/smartchoice/'):
            if fnmatch.fnmatch(filename, '*_' + context.args[0] + '_5G.png'):
                where_list.append(filename[:-12])
        if len(where_list) == 0:
            update.message.reply_text(context.args[0] + '년도에 측정된 행정동은 없습니다.')
        else:
            output_message = ', '.join(str(s) for s in where_list)
            update.message.reply_text(context.args[0] + '년 측정 대상 행정동입니다.\n' + output_message)
    else:
        update.message.reply_text('잘못된 입력입니다.\n/where 년도(4자리 숫자) 로 입력해주세요.\n예)/where 2020')


def when(update, context):
    if len(context.args) != 1:
        update.message.reply_text('잘못된 입력입니다.\n/when 행정동 으로 입력해주세요.\n예)/when 청담동')
    elif context.args[0].isnumeric():
        update.message.reply_text('잘못된 입력입니다.\n/where 년도 or /when 행정동 으로 입력해주세요.\n예)/where 2020, /when 청담동')

    elif isinstance(context.args[0], str):
        when_list = list()
        for filename in os.listdir('message/smartchoice/'):
            if fnmatch.fnmatch(filename, context.args[0] + '_*_5G.png'):
                when_list.append(filename[-11:-7])
        if len(when_list) == 0:
            update.message.reply_text(context.args[0] + '지역은 측정 이력이 없습니다.')
        else:
            output_message = ', '.join(str(s) for s in when_list)
            update.message.reply_text(context.args[0] + ' 지역이 측정된 년도입니다.\n' + output_message)
    else:
        update.message.reply_text('잘못된 입력입니다.\n/when 행정동 으로 입력해주세요.\n예)/when 청담동')


def helps(update, context):
    help_search = '/search 행정동 년도 : 해당 행정동의 해당 년도 측정결과 조회\n  - 예: /search 청담동 2020'
    help_when = '/when 행정동 : 해당 행정동이 측정된 년도 조회\n  - 예: /when 청담동'
    help_where = '/where 년도 : 해당 년도에 측정된 행정동 조회\n  - 예: /where 2020'
    help_inquiry = '/inquiry : 버튼식 조회 기능'
    output_message = help_when + '\n' + help_where + '\n' + help_search + '\n' + help_inquiry
    update.message.reply_text(output_message)
