from django.contrib import admin
from django.contrib import auth
from management.models import Morphology, LowThroughput, CenterInfo, morph_settings

###################################################################################################
# 어드민 페이지에서 관리정보를 추가/수정/삭제할 수 있도록 하기 위한 모듈
# [ 관리정보 리스트 ]
#  - 모폴러지(Morphology): 측정 데이터 내에 있는 부정확한 모폴러지를 수정하여 맵핑정보를 관리함
#  - 속도저하 기준(LowThroughput): 상황에 따라 변경되는 속도저하 기준 정보를 관리함 
#  - 센터정보(CenterInfo): 전국 14개 센터정보를 관리함
###################################################################################################
class MorphologyAdmin(admin.ModelAdmin):
    '''어드민 페이지에 모폴러지 정보를 보여주기 위한 클래스'''
    # form = PhoneForm
    list_display = ['userInfo2', 'morphology',]
    list_display_links = ['userInfo2',  'morphology', ]
    search_fields = ('userInfo2', )

class LowThroughputAdmin(admin.ModelAdmin):
    '''어드민 페이지에 속도저하(Low Throughput) 기준을 보여주기 위한 클래스'''
    # form = PhoneForm
    list_display = ['networkId', 'dataType', 'bandwidth',]
    list_display_links = ['networkId',]
    search_fields = ('networkId', )

class MorphSettingsAdmin(admin.ModelAdmin):
    '''어드민 페이지에 모폴로지 설정 추가'''
    list_display = ['morph', 'morph_startswith', 'morph_vulzone', 'fvg_dl_criteria', 'fvg_ul_criteria', 'lte_dl_criteria', 'lte_ul_criteria',\
                    'thg_dl_criteria', 'thg_ul_criteria', 'wifi_dl_criteria', 'wifi_ul_criteria']
    list_display_links = ['morph']

# -------------------------------------------------------------------------------------------------
# 금일 측정조 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class MeasureingTeamAdmin(admin.ModelAdmin):
    list_display = ['measdate_fmt', 'message']
    list_display_links = ['message']
    search_fields = ('message', 'message')
    list_filter = ['measdate',]
    ordering = ('-measdate', )

    def measdate_fmt(self, obj):
        return obj.measdate.strftime('%Y-%m-%d') # YYYY-MM-DD 표시 예) 2021-11-01

admin.site.register(Morphology, MorphologyAdmin) # 모폴러지 등록
admin.site.register(LowThroughput, LowThroughputAdmin) # 속도저하 기준 등록
admin.site.register(CenterInfo) # 센터정보 등록(전국 14개 센터)
admin.site.register(morph_settings, MorphSettingsAdmin)

# 사용자 인증관련 그룹을 어드민 페이지에서 제외한다.
admin.site.unregister(auth.models.Group)


