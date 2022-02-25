from django.contrib import admin
from django.contrib import auth
from management.models import Morphology, LowThroughput, CenterInfo

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

admin.site.register(Morphology, MorphologyAdmin) # 모폴러지 등록
admin.site.register(LowThroughput, LowThroughputAdmin) # 속도저하 기준 등록
admin.site.register(CenterInfo) # 센터정보 등록(전국 14개 센터)

# 사용자 인증관련 그룹을 어드민 페이지에서 제외한다.
admin.site.unregister(auth.models.Group)