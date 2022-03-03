from django.contrib import admin
from django.contrib import auth
from management.models import Morphology, SendFailure, LowThroughput, CenterInfo, MeasureingTeam

###################################################################################################
# 어드민 페이지에서 관리정보를 추가/수정/삭제할 수 있도록 하기 위한 모듈
# [ 관리정보 리스트 ]
#  - 모폴러지(Morphology): 측정 데이터 내에 있는 부정확한 모폴러지를 수정하여 맵핑정보를 관리함
#  - 속도저하 기준(LowThroughput): 상황에 따라 변경되는 속도저하 기준 정보를 관리함 
#  - 센터정보(CenterInfo): 전국 14개 센터정보를 관리함
#  - 전송실패 기준(SendFailure): 품질불량에 따른 전송실패 기준 정보를 관리함 
# -------------------------------------------------------------------------------------------------
###################################################################################################

# -------------------------------------------------------------------------------------------------
# 모폴러지 기준 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class MorphologyAdmin(admin.ModelAdmin):
    '''어드민 페이지에 모폴러지 정보를 보여주기 위한 클래스'''
    # form = PhoneForm
    list_display = ['userInfo2', 'morphology',]
    list_display_links = ['userInfo2',  'morphology', ]
    search_fields = ('userInfo2', )

# -------------------------------------------------------------------------------------------------
# 속도저하 기준 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class LowThroughputAdmin(admin.ModelAdmin):
    '''어드민 페이지에 속도저하(Low Throughput) 기준을 보여주기 위한 클래스'''
    # form = PhoneForm
    list_display = ['areaInd', 'networkId', 'dataType', 'bandwidth',]
    list_display_links = ['networkId',]
    search_fields = ('areaInd', 'networkId', )

# -------------------------------------------------------------------------------------------------
# 전송실패 기준 관리자 페이지 설정
# -------------------------------------------------------------------------------------------------
class SendFailureAdmin(admin.ModelAdmin):
    '''어드민 페이지에 전송실패(Send Failure) 기준을 보여주기 위한 클래스'''
    # form = PhoneForm
    list_display = ['areaInd', 'networkId', 'dataType', 'bandwidth',]
    list_display_links = ['networkId',]
    search_fields = ('areaInd', 'networkId', )

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
admin.site.register(SendFailure, SendFailureAdmin) # 전송실패 기준 등록
admin.site.register(LowThroughput, LowThroughputAdmin) # 속도저하 기준 등록
admin.site.register(CenterInfo) # 센터정보 등록(전국 14개 센터)

admin.site.register(MeasureingTeam, MeasureingTeamAdmin) # 금일 측정조

# 사용자 인증관련 그룹을 어드민 페이지에서 제외한다.
admin.site.unregister(auth.models.Group)