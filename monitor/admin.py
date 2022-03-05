from django.contrib import admin
from django import forms
from .models import Phone, MeasureCallData

###################################################################################################
# 어드민 페이지에서 모니터링 관련 정보를 보여주기 위한 모듈
# [ 측정 모니터링 ]
#  - 측정 단말, 측정 데이터(콜단위)
# [ 환경설정 관리 ]
#  - 센터정보, 모폴러지, 전송실패 기준, 속도저하 기준, 측정 보고주기, 금일측정조
# -------------------------------------------------------------------------------------------------
# 2022.02.25 - 측정 단말기 관리자 페이지의 화면상 항목들을 세션/그룹핑해서 표시 되도록 함
# 2022.03.03 - 측정 단말기 모폴러지 항목 추가 반영 
#             (측정 데이터의 모폴로지가 오입력 되는 경우 맵핑 테이블을 통해 재지정 하기 위함)
# 2022.03.05 - 측정 단말기 관리자 페이지 조회시 필터 기본값을 설정하기 위한 필터 클래스를 추가함
###################################################################################################
# class PhoneForm(forms.ModelForm):

#     def clean(self):
#         cleaned_data = self.cleaned_data
#         print(cleaned_data)
# -------------------------------------------------------------------------------------------------
# 측정 단말 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
class ManageFilter(SimpleListFilter):
    '''측정 단말기 관리자 페이지에서 필터 기본값을 지정하기 위한 클래스'''
    title = '관리대상'
    parameter_name = 'manage'
    default_value = 1 # 디폴트 필터값

    # 필터 항목중 '모두'를 없애기 위해서 함수를 오버라이딩 함
    # https://github.com/django/django/blob/main/django/contrib/admin/filters.py#L62
    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
            }

    # 보여질 필터 항목들을 정의한다.
    def lookups(self, request, model_admin):
        list_of_manage = [
            (0, _('아니요')),
            (1, _('예')),
        ]
        return sorted(list_of_manage, key=lambda tp: tp[1], reverse=True)

    # 선택된 필터 항목값에 따라 자료를 조회한다.
    def queryset(self, request, queryset):
        if self.value() in ('1', '0'):
            return queryset.filter(manage=self.value())
        return queryset

    # 측정 단말기를 조회하는 관리자 페이지를 처음 들어왔을 때 기본값으로 조회되게 한다.
    def value(self):
        value = super(ManageFilter, self).value()
        if value is None:
            if self.default_value is None:
                pass
            else:
                value = self.default_value
        return str(value)

class PhoneAdmin(admin.ModelAdmin):
    '''어드민 페이지에 측정단말 리스트를 보여주기 위한 클래스'''
    # form = PhoneForm
    list_display = ['userInfo1', 'morphology', 'phone_no', 'networkId', 'avg_downloadBandwidth_fmt', 'avg_uploadBandwidth_fmt', \
        'status', 'total_count', 'last_updated_at', 'active', 'manage']
    list_display_links = ['phone_no']
    search_fields = ('userInfo1', 'phone_no', )
    list_filter = ['active', ManageFilter,]

    # DL 평균속도를 소수점 2자리까지 화면에 표시한다. 
    def avg_downloadBandwidth_fmt(self, obj):
        return '%.2f' % obj.avg_downloadBandwidth

    avg_downloadBandwidth_fmt.short_description = 'DL'

    # UL 평균속도를 소수점 2자리까지 화면에 표시한다. 
    def avg_uploadBandwidth_fmt(self, obj):
        return '%.2f' % obj.avg_uploadBandwidth

    avg_uploadBandwidth_fmt.short_description = 'UL'


    # 2022.02.25 - 화면상의 항목들을 세션/그룹핑해서 보여준다. 
    fieldsets = (
        ('단말정보', {
            'fields': ('phone_no',
                        ('networkId', 'ispId'),
            ),
            # 'description' : '단말에 대한 정보를 보여줍니다.'
        }),
        ('측정정보', {
             'fields': (('userInfo1', 'morphology'),
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
        # filtered_query = query.filter(ispId='45008', manage=True)
        filtered_query = query.filter(ispId='45008')
        return filtered_query

    # def changelist_view(self, request, extra_context=None):
    #     if not request.GET.has_key('manage'):
    #         q = request.GET.copy()
    #         q['manage'] = 1
    #         request.GET = q
    #         request.META['QUERY_STRING'] = request.GET.urlencode()
    #     return super(PhoneAdmin,self).changelist_view(request, extra_context=extra_context)

    # 저장 버튼을 제외한 나머지 버튼들을 화면에서 보이지 않게 한다.
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
                'show_save': True,
                'show_save_and_add_another': False,
                'show_save_and_continue': False,
                'show_delete': False
            })
        return super().render_change_form(request, context, add, change, form_url, obj)


# -------------------------------------------------------------------------------------------------
# 측정 데이터(콜단위) 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
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


