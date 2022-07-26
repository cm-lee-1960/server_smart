from django.utils.html import format_html
from django.contrib import admin
from django.contrib import auth
from django.conf import settings
from .models import Morphology, SendFailure, LowThroughput, Center, MeasureingTeam, ReportCycle, MorphologyMap, \
    CenterManageArea, ChatMemberList, PhoneInfo, MorphologyDetail, MessageConfig, EtcConfig, MeasureArea

########################################################################################################################
# 어드민 페이지에서 관리정보를 추가/수정/삭제할 수 있도록 하기 위한 모듈
# [ 관리정보 리스트 ]
#  - 센터정보(Center): 전국 14개 센터정보를 관리함
#  - 모풀로지(Morphology): 모폴로지를 관리함(행정동, 테마, 인빌딩, 커버리지, 취약지구 등)
#  - 모폴로지 맵(MorphologyMap): 측정 데이터 내에 있는 부정확한 모풀로지를 수정하여 맵핑정보를 관리함
#  - 전송실패 기준(SendFailure): 품질불량에 따른 전송실패 기준 정보를 관리함 
#  - 속도저하 기준(LowThroughput): 상황에 따라 변경되는 속도저하 기준 정보를 관리함 
#  - 금일 측정조(MeasureingTeam): 당일 측정을 수행하는 측정조 현황을 입력 관리(측정 시작메시지에 포함됨)
#  - 측정 보고주기(ReportCycle): 측정 보고주기를 DB화 함(3, 10, 27, 37, 57)
#  - 센터별 관할지역(CenterManageArea): 지역센터별 관리대상 주소 정보
#  - 측정단말 사전정보(PhoneInfo): 측정단말 사전정보 (유형, 측정조)
# ----------------------------------------------------------------------------------------------------------------------
# 2022.03.13 - 관리자 페이지 앱들과 특정 앱의 모델들을 재정렬 한다.
# 2022.03.19 = 센터별 관할구역 관리자 페이지 추가
# 2022.03.28 - 센터정보 모델에 센터영문명(centerEngName) 항목 추가
# 2022.04.28 - 측정단말에 대한 사전정보 모델 추가
# 2022.06.29 - 측정단말 사전정보 관리자 페이지 수정
#              * 파워온/오프 항목이 앞단으로 배치하고, 최종 위치보고시간 항목 추가
#
########################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------
# 센터 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class CenterAdmin(admin.ModelAdmin):
    """어드민 페이지에 센터 정보를 보여주기 위한 클래스"""
    # # form = PhoneForm
    list_display = ['centerName', 'centerEngName', 'permissionLevel', 'senderNum', 'recipientOfficer', 'channelId',
                    'active', ]
    list_display_links = ['centerName',  'centerEngName', ]
    search_fields = ('centerName', 'centerEngName',)

    def get_ordering(self, request):
        return ['id']

# ----------------------------------------------------------------------------------------------------------------------
# 모풀로지 기준 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class MorphologyAdmin(admin.ModelAdmin):
    """어드민 페이지에 모풀로지 정보를 보여주기 위한 클래스"""
    # # form = PhoneForm
    list_display = ['id', 'morphology', 'manage', ]
    list_display_links = ['id', 'morphology', ]
    search_fields = ('id', 'morphology', )
    readonly_fields = ('id',)

# ----------------------------------------------------------------------------------------------------------------------
# 모풀로지 기준 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class MorphologyMapAdmin(admin.ModelAdmin):
    """어드민 페이지에 모풀로지 맵 정보를 보여주기 위한 클래스"""
    # # form = PhoneForm
    list_display = ['id', 'words', 'wordsCond', 'morphology', 'manage',]
    list_display_links = ['id', 'morphology', ]
    search_fields = ('wordsCond', 'morphology', )
    readonly_fields = ('id',)

# ----------------------------------------------------------------------------------------------------------------------
# 속도저하 기준 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class LowThroughputAdmin(admin.ModelAdmin):
    '''어드민 페이지에 속도저하(Low Throughput) 기준을 보여주기 위한 클래스'''
    # # form = PhoneForm
    list_display = ['id', 'areaInd', 'networkId', 'dataType', 'bandwidth',]
    list_display_links = ['id', 'networkId',]
    search_fields = ('areaInd', 'networkId', )
    readonly_fields = ('id',)

# ----------------------------------------------------------------------------------------------------------------------
# 전송실패 기준 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class SendFailureAdmin(admin.ModelAdmin):
    """어드민 페이지에 전송실패(Send Failure) 기준을 보여주기 위한 클래스"""
    # # form = PhoneForm
    list_display = ['id', 'areaInd', 'networkId', 'dataType', 'bandwidth',]
    list_display_links = ['id', 'networkId',]
    search_fields = ('areaInd', 'networkId', )
    readonly_fields = ('id',)


# ----------------------------------------------------------------------------------------------------------------------
# 금일 측정조 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class MeasureingTeamAdmin(admin.ModelAdmin):
    """어드민 페이지에 금일측정조(MeasureingTeam)을 보여주기 위한 클래스"""
    list_display = ['measdate_fmt', 'message']
    list_display_links = ['measdate_fmt', 'message']
    search_fields = ('message', 'message')
    list_filter = ['measdate',]
    ordering = ('-measdate', )

    def measdate_fmt(self, obj):
        return obj.measdate.strftime('%Y-%m-%d') # YYYY-MM-DD 표시 예) 2021-11-01

    measdate_fmt.short_description = '측정일자'


# ----------------------------------------------------------------------------------------------------------------------
# 측정 보고주기 관리자 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class ReportCycleAdmin(admin.ModelAdmin):
    """어드민 페이지에 측정 보고주기(ReportCycle)를 보여주기 위한 클래스"""
    list_display = ['reportCycle',]
    list_display_links = ['reportCycle']
    search_fields = ('id', 'reportCycle')
    readonly_fields = ('id',)

# ----------------------------------------------------------------------------------------------------------------------
# 센터별 관리구역
# ----------------------------------------------------------------------------------------------------------------------
class CenterManageAreaAdmin(admin.ModelAdmin):
    """어드민 페이지에 센터별 관할구역(CenterManageArea)를 보여주기 위한 클래스"""
    list_display = ['siDo', 'guGun', 'eupDong', 'address', 'addrType', 'bonbu', 'opCenter', 'center']
    list_display_links = ['address']
    search_fields = ('siDo', 'guGun', 'eupDong', 'address')
    list_filter = ['center',]
    ordering = ('center', )


# ----------------------------------------------------------------------------------------------------------------------
# 채팅 멤버 리스트 페이지 설정
# ----------------------------------------------------------------------------------------------------------------------
class ChatMemberListAdmin(admin.ModelAdmin):
    """어드민 페이지에 관리하는 채팅 멤버 리스트(ChatMemberList)를 보여주기 위한 클래스"""
    list_display = ['userchatId', 'firstName', 'lastName', 'userName', 'center', 'chatId', 'allowed', 'isBot']
    list_display_links = ['userchatId', ]
    #search_fields = ('userchatId', 'firstName', 'lastName', 'userName', 'center', 'chatId',)
    ist_filter = ['center', 'allowed']

    actions = ['set_all_true', ]

    # ---------------------------------------------------------------------------------------------
    # 허용여부를 일괄 True로 바꾸는 함수(채팅방 멤버 리스트  관리자 페이지에서 액션)
    # ---------------------------------------------------------------------------------------------
    def set_all_true(self, request, queryset):
        try:
            queryset.update(allowed=True)
        except:
            raise Exception("일괄변경 실패 - 선택한 컬럼을 확인하여주세요.")
    set_all_true.short_description = '선택한 인원 허용여부 True로 변경'

# ----------------------------------------------------------------------------------------------------------------------
# 측정단말 사전정보
# ----------------------------------------------------------------------------------------------------------------------
class PhoneInfoAdmin(admin.ModelAdmin):
    """어드민 페이지에 측정단말 사전정보(PhoneInfo)를 보여주기 위한 클래스"""
    list_display = ['power', 'networkId', 'mode', 'measuringTeam', 'phone_no_str', 'addressDetail_color', 'updated_at_str']
    list_display_links = ['phone_no_str']
    search_fields = ('networkId', 'mode', 'measuringTeam', )
    list_filter = ['networkId', 'mode', 'measuringTeam', ]
    # 정렬에는 @property를 사용할 수 없음
    ordering = ('networkId', 'mode', 'measuringTeam', 'phone_no', )

    def addressDetail_color(self, obj):
        if obj.power is True:
            color = 'yellow'
            return format_html(
                '<b style="background:{};">{}</b>',
                color,
                obj.addressDetail)
        else:
            return obj.addressDetail
    addressDetail_color.short_description = '최종위치'

    def updated_at_str(self, obj):
        # 참고: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        if obj.updated_at is not None:
            return obj.updated_at.strftime('%m/%d %H:%M')
        else:
            return ''
    updated_at_str.short_description = '최종 위치보고시간'

# ----------------------------------------------------------------------------------------------------------------------
# 모폴로지 상세 정보
# ----------------------------------------------------------------------------------------------------------------------
class MorphologyDetailAdmin(admin.ModelAdmin):
    """어드민 페이지에 모폴로지 상세를 보여주기 위한 클래스"""
    list_display = ['network_type', 'main_class', 'middle_class', 'sub_class', 'words_userInfo2', 'wordsCond_userInfo2', 'words_userInfo1', 'wordsCond_userInfo1']
    # list_display_links = ['main_class']
    search_fields = ('network_type', 'main_class', )
    list_filter = ['network_type', 'main_class', ]
    # 정렬에는 @property를 사용할 수 없음
    ordering = ('id', )
    fieldsets = (
        (None, {
            'fields': ('network_type', 'main_class', 'middle_class', 'sub_class',)
        }),
        ('대분류를 자동 구분하는 조건: 입력한 단어와 userInfo2를 비교하여 구분합니다. \n  * 단어는 쉼표+띄어쓰기(, )로 구분!!, 대문자만 사용', {
            'fields': ('words_userInfo2','wordsCond_userInfo2',)
        }),
        ('중분류를 자동 구분하는 조건: 입력한 단어와 userInfo1을 비교하여 구분합니다. // 대분류가 먼저 구분되어야 동작합니다. \n  * 단어는 쉼표+띄어쓰기(, )로 구분!!, 대문자만 사용', {
            'fields': ('words_userInfo1','wordsCond_userInfo1',)
        }),
    )


# ----------------------------------------------------------------------------------------------------------------------
# 측정지역  정보
# ----------------------------------------------------------------------------------------------------------------------
class MeasureAreaAdmin(admin.ModelAdmin):
    """어드민 페이지에 모폴로지 상세를 보여주기 위한 클래스"""
    list_display = ['area',]
    list_display_links = list_display
    search_fields = ('area',)
    list_filter = ['area',]

    ordering = ('id', )


# ----------------------------------------------------------------------------------------------------------------------
# 메시지 자동전송 여부
# ----------------------------------------------------------------------------------------------------------------------
class MessageConfigAdmin(admin.ModelAdmin):
    """어드민 페이지에 메시지 자동전송 여부(MessageConfig)를 보여주기 위한 클래스"""
    # list_display = ['eventFailure', 'eventLowThroughput', 'eventVoiceDrop', 'eventNR', 'evntOffZone', 'eventStay', 'eventDuplication', \
    #                 'START_F', 'START_M', 'MEASURING', 'END', 'END_LAST', 'ALL', ]
    list_display = ['settingName', 'booleanValue',]
    list_display_links = list_display
    ordering = ('id', )


# ----------------------------------------------------------------------------------------------------------------------
# 기타 환경설정
# ----------------------------------------------------------------------------------------------------------------------
class EtcConfigAdmin(admin.ModelAdmin):
    """어드민 페이지에 기타 환경설정(EtcConfig)를 보여주기 위한 클래스"""
    list_display = ['category', 'value_float', ]
    list_display_links = list_display
    ordering = ('category', 'id', )


# ----------------------------------------------------------------------------------------------------------------------
# 관리자 페이지에 모델을 등록한다.
# ----------------------------------------------------------------------------------------------------------------------
admin.site.register(Morphology, MorphologyAdmin) # 모풀로지 등록
admin.site.register(MorphologyMap, MorphologyMapAdmin) # 모풀로지 맵 등록
admin.site.register(SendFailure, SendFailureAdmin) # 전송실패 기준 등록
admin.site.register(LowThroughput, LowThroughputAdmin) # 속도저하 기준 등록
admin.site.register(Center, CenterAdmin) # 센터정보 등록(전국 14개 센터)
admin.site.register(MeasureArea, MeasureAreaAdmin) # 측정지역 등록(19개 지역)

admin.site.register(MeasureingTeam, MeasureingTeamAdmin) # 금일 측정조
admin.site.register(ReportCycle, ReportCycleAdmin) # 측정 보고주기
admin.site.register(CenterManageArea, CenterManageAreaAdmin) # 센터별 관할구역

admin.site.register(ChatMemberList, ChatMemberListAdmin) # 채팅방 멤버 리스트

admin.site.register(PhoneInfo, PhoneInfoAdmin) # 측정단말 사전정보
admin.site.register(MorphologyDetail, MorphologyDetailAdmin) # 측정단말 사전정보

admin.site.register(MessageConfig, MessageConfigAdmin) # 메시지 자동전송 여부
admin.site.register(EtcConfig, EtcConfigAdmin) # 기타 환경설정

# 사용자 인증관련 그룹을 어드민 페이지에서 제외한다.
admin.site.unregister(auth.models.Group)

# ----------------------------------------------------------------------------------------------------------------------
# 환경설정 관리(management) 모델 클래스를 정렬한다.
# ----------------------------------------------------------------------------------------------------------------------
def get_app_list(self, request):
    """환경설정 관리 모델 클래스를 정렬하는 함수"""
    app_dict = self._build_app_dict(request)
    #print(app_dict)
    # 관리자 페이지 앱들을 재정렬한다.
    ordering = settings.APPS_ORDERING
    app_list = sorted(app_dict.values(), key=lambda x: ordering[x['name']])
    for app in app_list:
        # 관리자 페이지 운영환경 관리의 모델들을 재정렬 한다. 
        if app['app_label'] == 'management':
            ordering = settings.MANAGEMENT_MODELS_ORDERING
            app['models'].sort(key=lambda x: ordering[x['name']])
    
    app_list.pop(4)
    return app_list

admin.AdminSite.get_app_list = get_app_list