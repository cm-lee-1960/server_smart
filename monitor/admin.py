from django.contrib import admin
from django import forms
from .models import Phone, MeasureCallData

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
    list_display = ['phone_no', 'userInfo1', 'networkId', 'avg_downloadBandwidth', \
        'avg_uploadBandwidth', 'status', 'total_count', 'last_updated_at', 'active']
    list_display_links = ['phone_no']
    search_fields = ('phone_no', )
    list_filter = ['active',]

    # 최종 위치보고시간을 출력한다(Integer -> String)
    def last_updated_at(self, phone):
        s = str(phone.last_updated)
        # 202201172315000
        return s[0:4]+'-'+s[4:6]+'-'+s[6:8]+' '+s[8:10]+':'+s[10:12]+':'+s[12:14]

    last_updated_at.short_description = '최종 위치보고시간'

    # 측정 단말기 중에서 KT 단말만 보여지게 한다. --- 최종확인 후 주석풀기 
    def get_queryset(self, request):
        query = super(PhoneAdmin, self).get_queryset(request)
        filtered_query = query.filter(ispId='45008', manage=True)
        return filtered_query

class DataAdmin(admin.ModelAdmin):
    '''어드민 페이지에 측정단말 데이터 건 by 건 보여주기 위한 클래스'''
    list_display = ['dataType', 'userInfo1', 'phone_no', 'currentCount', 'networkId', 'ispId', 'testNetworkType', \
        'downloadBandwidth', 'uploadBandwidth', 'meastime', 'userInfo2', 'addressDetail', 'cellId', 'isWifi',]
    list_display_links = ['phone_no']
    search_fields = ('phone_no', 'userInfo1')
    list_filter = ['userInfo1',]


class MonitorAdminArea(admin.AdminSite):
    '''관리자 페이지의 헤더 및 제목을 변경하기 위한 클래스'''
    # index_title = "단말상태 관리"
    # site_header = "스마트 상황실 관리"
    # site_title = "스마트 상활실"
    index_title = "smart2"
    site_header = "smart3"
    site_title = "smart4"


#monitor_site = MonitorAdminArea(name="스마트 상황실")
monitor_site = MonitorAdminArea(name="smart 1")

admin.site.register(Phone, PhoneAdmin)
monitor_site.register(Phone, PhoneAdmin)
admin.site.register(MeasureCallData, DataAdmin)
monitor_site.register(MeasureCallData, DataAdmin)

