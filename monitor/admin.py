from django.shortcuts import render
from django.contrib import admin, sites
from django.urls import path
from django.http import HttpResponseRedirect
from .models import PhoneGroup, Phone, MeasureCallData
from .close import measuring_end, measuring_day_close

###################################################################################################
# 어드민 페이지에서 모니터링 관련 정보를 보여주기 위한 모듈
# [ 측정 모니터링 ]
#  - 측정 단말기, 측정 데이터(콜단위)
# -------------------------------------------------------------------------------------------------
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
#
###################################################################################################

# -------------------------------------------------------------------------------------------------
# 단말 그룹 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class PhoneGroupAdmin(admin.ModelAdmin):
    """어드민 페이지에 단말그룹 리스트를 보여주기 위한 클래스"""
    list_display = ['measdate', 'phone_list', 'measuringTeam', 'userInfo1', 'active']
    list_display_links = ['phone_list', ]
    search_fields = ('measdate', 'userInfo1', 'phone_list', 'measuringTeam')
    list_filter = ['measdate', 'measuringTeam', 'active']
    actions = ['get_measuring_end_action']

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
        filtered_query = query.filter(ispId='45008')
        return filtered_query

    # 선택된 ROW를 삭제하는 액션을 삭제한다("선택된 측정 단말 을/를 삭제합니다.").
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # ---------------------------------------------------------------------------------------------
    # 측정단말 관리자 페이지에서 선택된 단말그룹에 대해 종료처리하는 액션 함수
    # ---------------------------------------------------------------------------------------------
    def get_measuring_end_action(self, request, queryset):
        """ 해당지역 측정을 종료하는 함수
            - 파라미터
              . queryset : 선택된 단말그룹에 대한 쿼리셋
            - 반환값: 없음
        """
        if queryset.exists():
            try: 
                result_list = []  # 여러개 그룹을 종료 시킬 수 있으므로 결과값을 리스트 선언
                # 관리자 페이지에서 넘겨 받은 쿼리셋에서 선택된 단말그룹을 하나씩 가져와서 측정종료 처리를 한다.
                for phoneGroup in queryset:
                    result = measuring_end(phoneGroup)
                    result_list.append(result)  # 결과 리스트 append
            except Exception as e:
                # 오류 코드 및 내용을 반환한다.
                print("get_measuring_end_action():", str(e))
                raise Exception("get_measuring_end_action(): %s" % e)

            #결과 메시지를 크로샷 전송 테스트 페이지로 넘긴다. (임시, 중복 종료 처리할 경우 결과 리스트의 첫 번째 메시지를 넘김)
            return render(request, 'message/xroshot_page.html', {'message' : result_list[0]['message']})

    get_measuring_end_action.short_description = '선택한 측정그룹 종료처리'

    # 당일측정 마감 버튼을 추가한다.
    change_list_template = "entities/heroes_changelist.html"
    # overriding get_urls -> 당일측정 마감 path 추가
    def get_urls(self):
        urls = super().get_urls()
        day_close_urls = [
            path('close/', self.day_close),
        ]
        return day_close_urls + urls
    # 버튼 클릭 시의 당일측정 마감 함수 실행  //  마감할 건이 없을 경우 예외처리 필요?
    def day_close(self, request):
        phoneGroup_list = self.model.objects.filter(active=True)  # 현재 Active 상태 단말그룹 리스트 추출
        measuring_day_close(phoneGroup_list)  # 당일 측정 마감 함수 실행
        self.message_user(request, "당일 측정이 마감되었습니다.")  # 실행 후 알람 메시지 생성
        return HttpResponseRedirect("../")

    change_list_template = "monitor/pg_change_list.html"

# -------------------------------------------------------------------------------------------------
# 측정 단말 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
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
                    'avg_downloadBandwidth_fmt', 'avg_uploadBandwidth_fmt', 'status', 'total_count', 
                    'last_updated_at', 'active', 'manage']
    list_display_links = ['phone_no_abbr']
    search_fields = ('userInfo1', 'phone_no', )
    list_filter = ['measdate', ManageFilter, 'active', ]

    list_per_page = 25 # 페이지당 데이터 건수 

    # DL 평균속도를 소수점 2자리까지 화면에 표시한다. 
    def avg_downloadBandwidth_fmt(self, obj):
        return '%.2f' % obj.avg_downloadBandwidth

    avg_downloadBandwidth_fmt.short_description = 'DL'

    # UL 평균속도를 소수점 2자리까지 화면에 표시한다. 
    def avg_uploadBandwidth_fmt(self, obj):
        return '%.2f' % obj.avg_uploadBandwidth

    avg_uploadBandwidth_fmt.short_description = 'UL'

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
        filtered_query = query.filter(ispId='45008')
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


# -------------------------------------------------------------------------------------------------
# 측정 데이터(콜단위) 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class MeasureCallDataAdmin(admin.ModelAdmin):
    """어드민 페이지에 측정단말 데이터 건 by 건 보여주기 위한 클래스"""
    list_display = ['userInfo1', 'phone_no', 'currentCount', 'networkId', 'ispId',\
                    'downloadBandwidth', 'uploadBandwidth', 'meastime_at', 'userInfo2', 'cellId',]
    list_display_links = ['phone_no']
    search_fields = ('userInfo1', 'phone_no', 'currentCount')
    list_filter = ['userInfo1',]
    ordering = ('userInfo1', 'phone_no', '-meastime', '-currentCount')

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
                'show_save': False,
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

admin.site.register(PhoneGroup, PhoneGroupAdmin) # 단말 그룹
admin.site.register(Phone, PhoneAdmin) # 측정 단말
admin.site.register(MeasureCallData, MeasureCallDataAdmin) # 측정 데이터(콜단위)





