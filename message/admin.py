from django.contrib import admin
from .models import SentTelegramMessage
from .tele_msg import TelegramBot

class SentTelegramMessageAdmin(admin.ModelAdmin):
    '''어드민 페이지에 보낸 메시지 정보를 보여주기 위한 클래스'''

    list_display = ['chat_type', 'chat_title', 'chat_message_id', 'chat_date', 'chat_text', 'is_del',]
    list_display_links = ['chat_text']
    search_fields = ('chat_type', 'chat_title', 'chat_date', 'chat_text', )
    list_filter = ['is_del',]
    actions = ['del_message_action', 'resend_message_action']

    list_per_page = 25 # 페이지당 데이터 건수 

    # ---------------------------------------------------------------------------------------------
    # 전송된 메시지를 회수하는 함수(전송 메시지 관리자 페이지에서 액션)
    # ---------------------------------------------------------------------------------------------
    def del_message_action(self, request, queryset):
      bot = TelegramBot()
      del_list = queryset.values_list('id', 'chat_id', 'chat_message_id')
      try:
        for id in del_list:
          result = bot.del_message(id[1], id[2])
          if result:
            queryset.filter(id=id[0]).update(is_del=True)
      except:
        print("회수 실패 - 메시지 선택을 확인하여주세요.")
        raise Exception("회수 실패 - 메시지 선택을 확인해주세요. \n 이미 회수된 메시지가 선택되어 있을 수 있습니다.")
    del_message_action.short_description = '선택한 메시지 회수'

    # ---------------------------------------------------------------------------------------------
    # 회수된 메시지를 재전송하는 함수(전송 메시지 관리자 페이지에서 액션)
    # ---------------------------------------------------------------------------------------------
    def resend_message_action(self, request, queryset):
      bot = TelegramBot()
      res_list = queryset.values_list('chat_id', 'chat_text')
      for id in res_list:
        bot.send_message_bot(id[0], id[1])
        # print(result)
        # if result.ok:
        #   queryset.filter(id=id[0]).update(is_del=False)
        # else:
        #   print("재전송 실패 - 메시지 선택을 확인하여주세요.")
        #   raise Exception("재전송 실패 - 메시지 선택을 확인해주세요. \n 이미 전송된 메시지가 선택되어 있을 수 있습니다.")
    resend_message_action.short_description = '선택한 메시지 재전송'

    # 저장 버튼을 제외한 나머지 버튼들을 화면에서 보이지 않게 한다.
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
                'show_save': True,
                'show_save_and_add_another': False,
                'show_save_and_continue': False,
                'show_delete': False
            })
        return super().render_change_form(request, context, add, change, form_url, obj)

    # 선택된 ROW를 삭제하는 액션을 삭제한다("선택된 측정 단말 을/를 삭제합니다.").
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(SentTelegramMessage, SentTelegramMessageAdmin)