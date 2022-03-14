from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MeasPlan

    
class MeasPlanAdmin(admin.ModelAdmin):
    '''어드민 페이지에 보낸 메시지 정보를 보여주기 위한 클래스'''

    list_display = ['year', 'networkId', 'area', 'molph_level0','meas_count']
    list_display_links = ['networkId']
    search_fields = ('year', 'networkId', 'area', 'molph_level0','meas_count')
    list_filter = ['year']
    actions = ['del_message_action', 'resend_message_action']

    list_per_page = 25 # 페이지당 데이터 건수 

admin.site.register(MeasPlan,MeasPlanAdmin)
   

