from django.contrib import admin
from django.contrib import auth
from django.conf import settings
from .models import Morphology, SendFailure, LowThroughput, Center, MeasureingTeam, ReportCycle, MorphologyMap, CenterManageArea

###################################################################################################
# 어드민 페이지에서 관리정보를 추가/수정/삭제할 수 있도록 하기 위한 모듈
# [ 관리정보 리스트 ]
#  - 센터정보(Center): 전국 14개 센터정보를 관리함
#  - 모풀로지(Morphology): 모폴로지를 관리함(행정동, 테마, 인빌딩, 커버리지, 취약지구 등)
#  - 모폴로지 맵(MorphologyMap): 측정 데이터 내에 있는 부정확한 모풀로지를 수정하여 맵핑정보를 관리함
#  - 전송실패 기준(SendFailure): 품질불량에 따른 전송실패 기준 정보를 관리함 
#  - 속도저하 기준(LowThroughput): 상황에 따라 변경되는 속도저하 기준 정보를 관리함 
#  - 금일 측정조(MeasureingTeam): 당일 측정을 수행하는 측정조 현황을 입력 관리(측정 시작메시지에 포함됨)
#  - 측정 보고주기(ReportCycle): 측정 보고주기를 DB화 함(3, 10, 27, 37, 57)
# -------------------------------------------------------------------------------------------------
# 2022.03.13 - 관리자 페이지 앱들과 특정 앱의 모델들을 재정렬 한다.
#
###################################################################################################

# -------------------------------------------------------------------------------------------------
# 센터 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class CenterAdmin(admin.ModelAdmin):
    """어드민 페이지에 센터 정보를 보여주기 위한 클래스"""
    # # form = PhoneForm
    list_display = ['centerName', 'centerName', 'permissionLevel', 'active', ]
    list_display_links = ['centerName',  ]
    search_fields = ('centerName', 'centerName',)

# -------------------------------------------------------------------------------------------------
# 모풀로지 기준 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class MorphologyAdmin(admin.ModelAdmin):
    """어드민 페이지에 모풀로지 정보를 보여주기 위한 클래스"""
    # # form = PhoneForm
    list_display = ['center', 'morphology', 'manage',]
    list_display_links = ['center', 'morphology', ]
    search_fields = ('center', 'morphology', )

# -------------------------------------------------------------------------------------------------
# 모풀로지 기준 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class MorphologyMapAdmin(admin.ModelAdmin):
    """어드민 페이지에 모풀로지 맵 정보를 보여주기 위한 클래스"""
    # # form = PhoneForm
    list_display = ['center', 'words', 'wordsCond', 'morphology', 'manage',]
    list_display_links = ['center', 'morphology', ]
    search_fields = ('center', 'morphology', )

# -------------------------------------------------------------------------------------------------
# 속도저하 기준 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class LowThroughputAdmin(admin.ModelAdmin):
    '''어드민 페이지에 속도저하(Low Throughput) 기준을 보여주기 위한 클래스'''
    # # form = PhoneForm
    list_display = ['center', 'areaInd', 'networkId', 'dataType', 'bandwidth',]
    list_display_links = ['networkId',]
    search_fields = ('areaInd', 'networkId', )

# -------------------------------------------------------------------------------------------------
# 전송실패 기준 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class SendFailureAdmin(admin.ModelAdmin):
    """어드민 페이지에 전송실패(Send Failure) 기준을 보여주기 위한 클래스"""
    # # form = PhoneForm
    list_display = ['center', 'areaInd', 'networkId', 'dataType', 'bandwidth',]
    list_display_links = ['networkId',]
    search_fields = ('areaInd', 'networkId', )


# -------------------------------------------------------------------------------------------------
# 금일 측정조 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class MeasureingTeamAdmin(admin.ModelAdmin):
    """어드민 페이지에 금일측정조(MeasureingTeam)을 보여주기 위한 클래스"""
    list_display = ['center', 'measdate_fmt', 'message']
    list_display_links = ['message']
    search_fields = ('message', 'message')
    list_filter = ['measdate',]
    ordering = ('-measdate', )

    def measdate_fmt(self, obj):
        return obj.measdate.strftime('%Y-%m-%d') # YYYY-MM-DD 표시 예) 2021-11-01

    measdate_fmt.short_description = '측정일자'


# -------------------------------------------------------------------------------------------------
# 측정 보고주기 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class ReportCycleAdmin(admin.ModelAdmin):
    """어드민 페이지에 측정 보고주기(ReportCycle)를 보여주기 위한 클래스"""
    list_display = ['center', 'reportCycle',]
    list_display_links = ['center', 'reportCycle']
    search_fields = ('center', 'reportCycle')
    list_filter = ['center',]


# -------------------------------------------------------------------------------------------------
# 센터별 관리구역
# -------------------------------------------------------------------------------------------------
class CenterManageAreaAdmin(admin.ModelAdmin):
    """어드민 페이지에 센터별 관할구역(CenterManageArea)를 보여주기 위한 클래스"""
    list_display = ['siDo', 'guGun', 'eupDong', 'address', 'addrType', 'bonbu', 'opCenter', 'center']
    list_display_links = ['address']
    search_fields = ('siDo', 'guGun', 'eupDong', 'address')
    list_filter = ['siDo',]
    # ordering = ('-measdate', )


admin.site.register(Morphology, MorphologyAdmin) # 모풀로지 등록
admin.site.register(MorphologyMap, MorphologyMapAdmin) # 모풀로지 맵 등록
admin.site.register(SendFailure, SendFailureAdmin) # 전송실패 기준 등록
admin.site.register(LowThroughput, LowThroughputAdmin) # 속도저하 기준 등록
admin.site.register(Center, CenterAdmin) # 센터정보 등록(전국 14개 센터)

admin.site.register(MeasureingTeam, MeasureingTeamAdmin) # 금일 측정조
admin.site.register(ReportCycle, ReportCycleAdmin) # 측정 보고주기
admin.site.register(CenterManageArea, CenterManageAreaAdmin) # 센터별 관할구역

# 사용자 인증관련 그룹을 어드민 페이지에서 제외한다.
admin.site.unregister(auth.models.Group)

# 환경설정 관리 모델 클래스를 정렬한다.
def get_app_list(self, request):
    """환경설정 관리 모델 클래스를 정렬하는 함수"""
    app_dict = self._build_app_dict(request)
    # 관리자 페이지 앱들을 재정렬한다.
    ordering = settings.APPS_ORDERING
    app_list = sorted(app_dict.values(), key=lambda x: ordering[x['name']])
    for app in app_list:
        # 관리자 페이지 운영환경 관리의 모델들을 재정렬 한다. 
        if app['app_label'] == 'management':
            ordering = settings.MANAGEMENT_MODELS_ORDERING
            app['models'].sort(key=lambda x: ordering[x['name']])

    return app_list

admin.AdminSite.get_app_list = get_app_list