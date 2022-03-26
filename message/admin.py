from django.contrib import admin
from .models import SentTelegramMessage
from .tele_msg import TelegramBot

########################################################################################################################
# 전송된 텔레그램 메시지를 취소하거나 재전송하기 위한 관리자 페이지
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.19 - 코드 및 주석 작성 룰에 벗어난 내용 수정
#            - 주고 받는 파라미터들을 객체로 하여 의미를 쉽게 파악할 수 있도록 수정함
#
########################################################################################################################
class SentTelegramMessageAdmin(admin.ModelAdmin):
    """어드민 페이지에 보낸 메시지 정보를 보여주기 위한 클래스"""

    list_display = ['chat_type', 'chat_title', 'chat_message_id', 'chat_date', 'chat_text', 'is_del',]
    list_display_links = ['chat_text']
    search_fields = ('chat_type', 'chat_title', 'chat_date', 'chat_text', )
    list_filter = ['is_del',]
    actions = ['delete_message_action', 'resend_message_action']

    list_per_page = 25 # 페이지당 데이터 건수 

    # ------------------------------------------------------------------------------------------------------------------
    # 전송된 메시지를 회수하는 함수(전송 메시지 관리자 페이지에서 액션)
    # 2022.03.19 - 주고 받는 파라미터들을 객체로 하여 의미를 쉽게 파악할 수 있도록 수정함
    # ------------------------------------------------------------------------------------------------------------------
    def delete_message_action(self, request, queryset):
        """전송된 메시지를 취소하는 함수"""
        bot = TelegramBot()
        try:
            for sentMessage in queryset:
                # 전송된 메시지를 취소한다.
                result = bot.delete_message(sentMessage.chat_id, sentMessage.chat_message_id)
                # 취소가 성공하면 전송취소여부를 업데이트 한다.
                if result:
                    sentMessage.is_del = True
                    sentMessage.save()
        except Exception as e:
            # 오류 코드 및 내용을 반환한다.
            print("delete_message_action():", str(e))
            raise Exception("delete_message_action(): %s" % e)
    delete_message_action.short_description = '선택한 메시지 회수'

    # ------------------------------------------------------------------------------------------------------------------
    # 회수된 메시지를 재전송하는 함수(전송 메시지 관리자 페이지에서 액션)
    # 2022.03.19 - 주고 받는 파라미터들을 객체로 하여 의미를 쉽게 파악할 수 있도록 수정함
    # ------------------------------------------------------------------------------------------------------------------
    def resend_message_action(self, request, queryset):
        """선택된 메시지를 재정송하는 함수"""
        bot = TelegramBot()
        for deletedMessage in queryset:
            # 선택된 메시지를 재전송한다.
            bot.send_message_bot(deletedMessage.chat_id, deletedMessage.chat_text)
    resend_message_action.short_description = '선택한 메시지 재전송'

    # ------------------------------------------------------------------------------------------------------------------
    # 저장 버튼을 제외한 나머지 버튼들을 화면에서 보이지 않게 한다.
    # ------------------------------------------------------------------------------------------------------------------
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
                'show_save': True,
                'show_save_and_add_another': False,
                'show_save_and_continue': False,
                'show_delete': False
            })
        return super().render_change_form(request, context, add, change, form_url, obj)

    # ------------------------------------------------------------------------------------------------------------------
    # 선택된 ROW를 삭제하는 액션을 삭제한다("선택된 측정 단말 을/를 삭제합니다.").
    # ------------------------------------------------------------------------------------------------------------------
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(SentTelegramMessage, SentTelegramMessageAdmin)