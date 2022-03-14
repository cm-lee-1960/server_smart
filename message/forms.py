from django import forms
from .models import SentXroshotMessage

# class XroshotMessage(froms.Form):
#     ''' 크로샷 메시지 DB '''
#     messasge = forms.CharField(help_text="메시지 내용을 입력 해주세요.", verbose_name="내용")
#     receiver = forms.CharField(
#         help_text="수신자 전화번호를 입력 해주세요. 쉼표(,)로 구분하여 입력 해주세요.", \
#         error_messages="전화번호를 잘못 입력하였습니다. 쉼표로 구분되었는지 확인 해주세요.", \
#         verbose_name="번호")
#     send_date = forms.DateTimeField(required=False, blank=True, auto_now_add=True, verbose_name='송신시간')


class SentXroshotMessageForm(forms.ModelForm):
    class Meta:
        model = SentXroshotMessage
        fields = ['id', 'message','receiver', 'result']
        