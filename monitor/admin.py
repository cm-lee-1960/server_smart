from django.shortcuts import render
from django.contrib import admin
from django.db.models import Q
from .models import PhoneGroup, Phone, MeasureCallData, Message
from .close import measuring_end

########################################################################################################################
# 어드민 페이지에서 모니터링 관련 정보를 보여주기 위한 모듈
# [ 측정 모니터링 ]
#  - 측정 단말기, 측정 데이터(콜단위)
# ----------------------------------------------------------------------------------------------------------------------
# 2022.02.25 - 측정 단말기 관리자 페이지의 화면상 항목들을 세션/그룹핑해서 표시 되도록 함
# 2022.03.03 - 측정 단말기 모풀로지 항목 추가 반영 
#             (측정 데이터의 모폴로지가 오입력 되는 경우 맵핑 테이블을 통해 재지정 하기 위함)
# 2022.03.05 - 측정 단말기 관리자 페이지 조회시 필터 기본값을 설정하기 위한 필터 클래스를 추가함
# 2022.03.06 - 3.5 작성한 필터 클래스 보완
#            - 측정단말 관리자 페이지를 처음 들어갈 때 관리대상만 보여지게 하고, 이후 필터조건에 따라 조회되게 함
#              (필터조건: 예, 아니요, 모두)
#            - 측정단말의 전화번호 끝 4자리만 표기, 측정단말 관리자 상세화면에서 필드 항목의 사이즈 조정
# 2022.03.10 - 단말그룹 관리자 페이지 추가 (단말그룹에 측정조를 입력할 수 있도록 함)
# 2022.03.17 - 단말그룹 관리자 페이지에서 선택된 단말그룹에 대해 측정종료 처리 함수를 추가함
# 2022.03.22 - 단말그룹에 관리대상 여부를 추가하고 관리대상 자료만 관리자 화면에 조회도록 수정함
# 2022.03.24 - 측정종료 및 측정마감 모듈을 홈페이지에서 호출할 수 있도록 측정 모니터링앱(monitor) 뷰 함수로 이동
# 2022.03.29 - 단말그룹 관리자 페이지에 DL/UL콜수, DL/UL속도, LTE전환율, 이벤트발생 건수 등 항목 추가
# 2022.06.16 - 단말그룹 날짜필드로 일자별 사전검색 기능 추가
#
########################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------
# 단말그룹 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class PhoneGroupAdmin(admin.ModelAdmin):
    """어드민 페이지에 단말그룹 리스트를 보여주기 위한 클래스"""
    list_display = ['measdate', 'phone_list', 'networkId', 'measuringTeam', 'userInfo1', 'morphology',
                    'dl_count', 'ul_count', 'downloadBandwidth_fmt', 'uploadBandwidth_fmt', 'nr_percent',
                    'event_count', 'active', 'manage']
    list_display_links = ['phone_list', ]
    search_fields = ('measdate', 'userInfo1', 'networkId', 'measuringTeam')
    list_filter = ['measdate', 'measuringTeam', 'active', 'manage']
    actions = ['get_measuring_end_action']
    ordering = ('-measdate', '-manage', 'measuringTeam', 'userInfo1', )

    list_per_page = 25 # 페이지당 데이터 건수
    date_hierarchy = 'last_updated_dt'

    # DL 평균속도를 소수점 2자리까지 화면에 표시한다.
    def downloadBandwidth_fmt(self, obj):
        return '%.1f' % obj.downloadBandwidth

    downloadBandwidth_fmt.short_description = 'DL속도'

    # UL 평균속도를 소수점 2자리까지 화면에 표시한다.
    def uploadBandwidth_fmt(self, obj):
        return '%.1f' % obj.uploadBandwidth

    uploadBandwidth_fmt.short_description = 'UL속도'

    # DetailView에서 적용하는 내용임
    # formfield_overrides = {
    #     models.CharField: {'widget': TextInput(attrs={'size':'20'})},
    #     models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    # }

    # 해당 단말그룹에 묶여 있는 단말기 번호를 가져온다.
    def phone_list(self, phoneGroup):
        p_list = []
        for phone in phoneGroup.phone_set.all():
            p_list.append(str(phone.phone_no)[-4:])
        return ','.join(p_list)

    phone_list.short_description = '단말번호'

    # 단말그룹 중에서 KT 자료만 보여지게 한다.
    def get_queryset(self, request):
        query = super(PhoneGroupAdmin, self).get_queryset(request)
        filtered_query = query.filter( Q(manage=True) | Q(ispId='45008') )
        return filtered_query

    # 선택된 ROW를 삭제하는 액션을 삭제한다("선택된 측정 단말 을/를 삭제합니다.").
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


# ----------------------------------------------------------------------------------------------------------------------
# 측정단말 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter

class ManageFilter(SimpleListFilter):
    """측정 단말기 관리자 페이지에서 필터 기본값을 지정하기 위한 클래스"""
    # 2022.03.06 - 하고 싶은 것은 측정단말을 조회했을 때, 관리대상 측정단말 리스트만 보여지게 하고 싶음
    #              즉, 측정단말 관리자 페이지를 처음 들어갔을 때는 관리대상만 보여지고, 필터를 통해 조회할 때는
    #              각각 필터조건에 맞게 조회하고 싶음
    #            - 어떻게 어떻게 해서 구현은 했는데, 왠지 로직이 좋아 보이지는 않음
    title = '관리대상'
    parameter_name = 'manage'
    default_value = None

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
            (2, _('모두'))
        ]
        return sorted(list_of_manage, key=lambda tp: tp[1], reverse=True)

    def queryset(self, request, queryset):
        if self.value() == '2':
            pass
        elif self.value() == 'None':
            return queryset.filter(manage=1)
        elif self.value():
            return queryset.filter(manage=self.value())
        return queryset

    def value(self):
        value = super(ManageFilter, self).value()
        if value is None:
            if self.default_value is None:
                value = None
                self.default_value = value
            else:
                value = self.default_value
        return str(value) 


class PhoneAdmin(admin.ModelAdmin):
    """어드민 페이지에 측정단말 리스트를 보여주기 위한 클래스"""
    # form = PhoneForm
    list_display = ['measdate', 'userInfo1', 'userInfo2', 'morphology', 'phone_no_abbr', 'networkId', 
                    'downloadBandwidth_fmt', 'uploadBandwidth_fmt', 'status', 'total_count',
                    'last_updated_at', 'active', 'manage']
    list_display_links = ['phone_no_abbr']
    search_fields = ('userInfo1', 'phone_no', )
    list_filter = ['measdate', ManageFilter, 'active', ]

    list_per_page = 25 # 페이지당 데이터 건수
    # date_hierarchy = 'last_updated_dt'

    # DL 평균속도를 소수점 2자리까지 화면에 표시한다. 
    def downloadBandwidth_fmt(self, obj):
        return '%.1f' % obj.downloadBandwidth

    downloadBandwidth_fmt.short_description = 'DL속도'

    # UL 평균속도를 소수점 2자리까지 화면에 표시한다. 
    def uploadBandwidth_fmt(self, obj):
        return '%.1f' % obj.uploadBandwidth

    uploadBandwidth_fmt.short_description = 'UL속도'

    # 2022.03.06 - 측정 단말기의 상세화면에서 특정 항목의 길이를 조정한다.
    def get_form(self, request, obj=None, **kwargs):
        form = super(PhoneAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['userInfo1'].widget.attrs['style'] = 'width: 15em;'
        form.base_fields['userInfo2'].widget.attrs['style'] = 'width: 10em;'
        return form

    # 2022.02.25 - 화면상의 항목들을 세션/그룹핑해서 보여준다. 
    fieldsets = (
        ('단말정보', {
            'fields': ('phone_no',
                        ('networkId', 'ispId'),
            ),
            # 'description' : '단말에 대한 정보를 보여줍니다.'
        }),
        ('측정정보', {
             'fields': (('userInfo1', 'userInfo2', 'morphology'),
                        ('downloadBandwidth', 'uploadBandwidth'),
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

    # 전화번호는 뒷 4자리만 출력한다.
    def phone_no_abbr(self, phone):
        return str(phone.phone_no)[-4:]
    
    phone_no_abbr.short_description = '전화번호'

    # 최종 위치보고시간을 출력한다(Integer -> String)
    def last_updated_at(self, phone):
        s = str(phone.last_updated)
        # 202201172315000
        return s[0:4]+'-'+s[4:6]+'-'+s[6:8]+' '+s[8:10]+':'+s[10:12]+':'+s[12:14]

    last_updated_at.short_description = '최종 위치보고시간'

    # 측정 단말기 중에서 KT 단말만 보여지게 한다.
    def get_queryset(self, request):
        query = super(PhoneAdmin, self).get_queryset(request)
        # filtered_query = query.filter(ispId='45008', manage=True)
        filtered_query = query.filter( Q(manage=True) | Q(ispId='45008') )
        return filtered_query

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


# ----------------------------------------------------------------------------------------------------------------------
# 측정 데이터(콜단위) 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class MeasureCallDataAdmin(admin.ModelAdmin):
    """어드민 페이지에 측정단말 데이터 건 by 건 보여주기 위한 클래스"""
    list_display = ['measdate', 'userInfo1', 'phone_no', 'currentCount', 'networkId', 'ispId',\
                    'downloadBandwidth', 'uploadBandwidth', 'meastime_at', 'userInfo2', 'cellId',]
    list_display_links = ['phone_no']
    search_fields = ('userInfo1', 'phone_no', 'currentCount')
    list_filter = ['userInfo1',]
    ordering = ('-meastime', 'userInfo1', 'phone_no', '-meastime', '-currentCount')

    list_per_page = 25 # 페이지당 데이터 건수

    # 측정시간을 출력한다(Integer -> String)
    def meastime_at(self, mdata):
        s = str(mdata.meastime)
        # 202201172315000
        return s[8:10]+':'+s[10:12]+':'+s[12:14]

    meastime_at.short_description = '측정시간'

    # 측정 단말기 중에서 KT 단말만 보여지게 한다. --- 최종확인 후 주석풀기 
    def get_queryset(self, request):
        query = super(MeasureCallDataAdmin, self).get_queryset(request)
        filtered_query = query.filter(ispId='45008', testNetworkType='speed')
        return filtered_query

    # 모든 버튼을 보이지 않게 한다.
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
                'show_save': True,
                'show_save_and_add_another': False,
                'show_save_and_continue': False,
                'show_delete': False
            })
        return super().render_change_form(request, context, add, change, form_url, obj)

    # 선택된 ROW를 삭제하는 액션을 삭제한다("선택된 측정 데이터(콜단위) 을/를 삭제합니다.").
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

# ----------------------------------------------------------------------------------------------------------------------
# 텔레그램 전송메시지 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class MessageAdmin(admin.ModelAdmin):
    list_display = ['measdate', 'center', 'status', 'messageType', 'message', 'sended', 'sendTime', 'isDel']
    search_fields = ('message', )

    list_per_page = 25 # 페이지당 데이터 건수
    date_hierarchy = 'sendTime'

admin.site.register(PhoneGroup, PhoneGroupAdmin) # 단말 그룹
admin.site.register(Phone, PhoneAdmin) # 측정 단말
admin.site.register(MeasureCallData, MeasureCallDataAdmin) # 측정 데이터(콜단위)
admin.site.register(Message, MessageAdmin) # 측정 데이터(콜단위)





