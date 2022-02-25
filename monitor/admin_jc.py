from django.contrib import admin
from django import forms
from .models import Phone, PhoneGroup

# class PhoneForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(PhoneForm, self).__init__(*args, **kwargs)
#         # self.fields['phoneGroup'].editable = False
#         self.fields['phoneGroup'].widget.attrs['readonly'] = True
#     class Meta:
#         model = Phone
#         fields = '__all__'
class PhoneAdmin(admin.ModelAdmin):
    '''어드민 페이지에 측정단말 리스트를 보여주기 위한 클래스'''
    # form = PhoneForm
    list_display = ['phone_type', 'phone_no', 'networkId', 'avg_downloadBandwidth', \
        'avg_uploadBandwidth', 'status', 'total_count', 'userInfo1', 'last_updated_at', 'active']
    list_display_links = ['phone_no']
    search_fields = ('phone_no', 'userInfo1', 'total_count')
    list_filter = ['active',]

    # 최종 위치보고시간을 출력한다(Integer -> String)
    def last_updated_at(self, phone):
        s = str(phone.last_updated)
        # 202201172315000
        return s[0:4]+'-'+s[4:6]+'-'+s[6:8]+' '+s[8:10]+':'+s[10:12]+':'+s[12:14]

    last_updated_at.short_description = '최종 위치보고시간'

class PhoneGroupAdmin(admin.ModelAdmin):
    '''어드민 페이지에 측정그룹 리스트를 보여주기 위한 클래스'''
    # form = PhoneForm
    list_display = ['userInfo1', 'phone_no', 'ispId', 'active', \
        'measure_type', 'type_count', 'msg_sended', 'created_at']
    list_display_links = ['userInfo1']
    search_fields = ('userInfo1', 'phone_no', )
    list_filter = ['userInfo1',]

class MonitorAdminArea(admin.AdminSite):
    '''관리자 페이지의 헤더 및 제목을 변경하기 위한 클래스'''
    index_title = "단말상태 관리"
    site_header = "스마트 상황실 관리"
    site_title = "스마트 상활실"

monitor_site = MonitorAdminArea(name="스마트 상황실")

admin.site.register(Phone, PhoneAdmin)
admin.site.register(PhoneGroup, PhoneGroupAdmin)
monitor_site.register(Phone, PhoneAdmin)
monitor_site.register(PhoneGroup, PhoneGroupAdmin)

