from django.contrib import admin
from django import forms
from .models import Phone, MeasureCallData

###################################################################################################
# 어드민 페이지에서 모니터링 관련 정보를 보여주기 위한 모듈
# [ 모니터링 리스트 ]
#  - 측정 단말
#  - 측정 데이터(콜단위)
###################################################################################################
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
    list_display = ['userInfo1', 'phone_no', 'networkId', 'avg_downloadBandwidth', \
        'avg_uploadBandwidth', 'status', 'total_count', 'last_updated_at', 'active']
    list_display_links = ['phone_no']
    search_fields = ('phone_no', )
    list_filter = ['active',]

    # 2020.02.25 화면상에 항목들을 그룹핑해서 보여준다. 
    # fields = [ 'phone_no',
    #             ('networkId', 'ispId'),
    #             'userInfo1',
    #             ('avg_downloadBandwidth', 'avg_uploadBandwidth'), 
    #             ('dl_count', 'ul_count'),
    #             ('status', 'total_count'),
    #             'last_updated', 
    #             'manage',
    #             'active',
    #         ]

    # 2022.02.25 화면상의 항목들을 세션/그룹핑해서 보여준다. 
    fieldsets = (
        ('단말정보', {
            'fields': ('phone_no',
                        ('networkId', 'ispId'),
            ),
            # 'description' : '단말에 대한 정보를 보여줍니다.'
        }),
        ('측정정보', {
             'fields': ('userInfo1',
                        ('avg_downloadBandwidth', 'avg_uploadBandwidth'), 
                        ('dl_count', 'ul_count'),
                        ('status', 'total_count'),
                        'last_updated', 
            ),
        }),
        ('상태정보', {
            'fields': ('manage',
                        'active', 
            ),
            # 'classes': ('collapse',),
        }),
    )

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

    # def has_delete_permission(self, request, obj=None):
    #     # return request.phone.is_superuser()
    #     return False

    # 저장 버튼을 제외한 나머지 버튼들을 화면에서 보이지 않게 한다.
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
                'show_save': True,
                'show_save_and_add_another': False,
                'show_save_and_continue': False,
                'show_delete': False
            })
        return super().render_change_form(request, context, add, change, form_url, obj)


class MeasureCallDataAdmin(admin.ModelAdmin):
    '''어드민 페이지에 측정단말 데이터 건 by 건 보여주기 위한 클래스'''
    list_display = ['userInfo1', 'phone_no', 'currentCount', 'networkId', 'ispId',\
                    'downloadBandwidth', 'uploadBandwidth', 'meastime', 'userInfo2', 'addressDetail', 'cellId', 'isWifi',]
    list_display_links = ['phone_no']
    search_fields = ('phone_no', '-currentCount')
    list_filter = ['userInfo1',]
    ordering = ('userInfo1', 'phone_no', '-currentCount')

    # 측정 단말기 중에서 KT 단말만 보여지게 한다. --- 최종확인 후 주석풀기 
    def get_queryset(self, request):
        query = super(MeasureCallDataAdmin, self).get_queryset(request)
        filtered_query = query.filter(ispId='45008', testNetworkType='speed')
        return filtered_query

class MonitorAdminArea(admin.AdminSite):
    '''관리자 페이지의 헤더 및 제목을 변경하기 위한 클래스'''
    index_title = "단말상태 관리"
    site_header = "스마트 상황실 관리"
    site_title = "스마트 상활실"

monitor_site = MonitorAdminArea(name="스마트 상황실")

admin.site.register(Phone, PhoneAdmin) # 측정 단말
monitor_site.register(Phone, PhoneAdmin) # 측정 단말 -- 어드민 페이지 별도분리 테스트
admin.site.register(MeasureCallData, MeasureCallDataAdmin) # 측정 데이터(콜단위)
monitor_site.register(MeasureCallData, MeasureCallDataAdmin) # 측정 데이터(콜단위) -- 어드민 페이지 별도분리 테스트

