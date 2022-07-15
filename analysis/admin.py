from django.contrib import admin
from django.contrib import auth
from django.conf import settings
from .models import MeasPlan,MeasLastyear5G,MeasLastyearLTE,MeasLastyearWiFi,LastMeasDayClose,ReportMessage,PostMeasure5G,PostMeasureLTE,MeasLastyeardistrict,MeasLastyearWeak

    
# class MeasPlanAdmin(admin.ModelAdmin):
#     '''어드민 페이지에 보낸 메시지 정보를 보여주기 위한 클래스'''

#     list_display = ['year', 'networkId', 'area', 'molph_level0','meas_count']
#     list_display_links = ['networkId']
#     search_fields = ('year', 'networkId', 'area', 'molph_level0','meas_count')
#     list_filter = ['year']
#     actions = ['del_message_action', 'resend_message_action']

#     list_per_page = 25 # 페이지당 데이터 건수 

# admin.site.register(MeasPlan,MeasPlanAdmin)
   
# class MeasResultAdmin(admin.ModelAdmin):
#     '''어드민 페이지에 보낸 메시지 정보를 보여주기 위한 클래스'''

#     list_display = ['date', 'info', 'networkId', 'area', 'molph_level0', 'molph_level1']
#     list_display_links = ['networkId']
#     search_fields = ('date', 'networkId', 'area', 'molph_level0')
#     list_filter = ['date', 'info', 'networkId']
#     actions = ['del_message_action', 'resend_message_action']
    
#     list_per_page = 25 # 페이지당 데이터 건수 

# admin.site.register(MeasResult,MeasResultAdmin)

class MeasPlanAdmin(admin.ModelAdmin):
    '''대상등록을 위한 클래스'''
    
    model = MeasPlan
    list_display = ['planYear','nsahjd5G','nsadg5G','sa5G','nsapublic5G','cv5G','bctLTE','mctLTE','sctLTE','ibLTE','tmLTE','cvLTE','syWiFi','gbWiFi','publicWiFi',
                    'dsrWeak','yghrWeak','yidsWeak','hadrWeak','totalnsa5G','total5G','totalLTE','totalWiFi','totalWeakArea','total',]
    list_display_links = ['planYear',]
    search_fields = ('planYear',)

class MeasLastyear5GAdmin(admin.ModelAdmin):
    '''대상등록을 위한 클래스'''
   
    model = MeasLastyear5G
    list_display = ['measYear','measarea','DL','UL','LTEDL','LTEUL','delay',]
    list_display_links = ['measarea',]
    search_fields = ('measarea',)

class MeasLastyearLTEAdmin(admin.ModelAdmin):
    '''대상등록을 위한 클래스'''
    
    model = MeasLastyearLTE
    list_display = ['measYear','measarea','DL','UL','delay',]
    list_display_links = ['measarea',]
    search_fields = ('measarea',)
    
class MeasLastyeardistrictAdmin(admin.ModelAdmin):
    '''대상등록을 위한 클래스'''
    
    model = MeasLastyeardistrict
    list_display = ['measYear','nettype','district','KTDL','SKTDL','LGDL']
    list_display_links = ['nettype','district',]
    search_fields = ('nettype','district',)

class MeasLastyearWiFiAdmin(admin.ModelAdmin):
    '''대상등록을 위한 클래스'''
    
    model = MeasLastyearWiFi
    list_display = ['measYear','WiFitype','DL','UL',]
    list_display_links = ['WiFitype',]
    search_fields = ('WiFitype',)
    
class LastMeasDayCloseAdmin(admin.ModelAdmin):
    '''대상등록을 위한 클래스'''
    
    model = LastMeasDayClose
    list_display = ['measdate','userInfo1','nettype','mopho','detailadd','center','district','downloadBandwidth','uploadBandwidth','dl_nr_percent','ul_nr_percent','udpJitter','plus','subadd']
    list_display_links = ['measdate','userInfo1',]
    search_fields = ('measdate','userInfo1',)
    list_per_page = 25 # 페이지당 데이터 건수

class ReportMessageAdmin(admin.ModelAdmin):
    '''대상등록을 위한 클래스'''
    
    model = ReportMessage
    list_display = ['measdate','msg5G',
    'msgLTE',
    'msgWiFi',
    'msgWeak',
    'msg5Gafter',
    'msgLTEafter',]
    list_display_links = ['msg5G',]
    search_fields = ('msg5G',)

class PostMeasure5GAdmin(admin.ModelAdmin):
    '''대상등록을 위한 클래스'''
    
    model = PostMeasure5G
    list_display = ['measdate',
    'district',
    'name',
    'measkt_dl',
    'measkt_ul',
    'measkt_rsrp',
    'measkt_lte',
    'postmeaskt_dl',
    'postmeaskt_ul',
    'postmeaskt_rsrp',
    'postmeaskt_lte',
    'postmeasskt_dl',
    'postmeasskt_ul',
    'postmeasskt_rsrp',
    'postmeasskt_lte',
    'postmeaslg_dl',
    'postmeaslg_ul',
    'postmeaslg_rsrp',
    'postmeaslg_lte',]
    list_display_links = ['name',]
    search_fields = ('name','measdate')    

class PostMeasureLTEAdmin(admin.ModelAdmin):
    '''대상등록을 위한 클래스'''
    
    model = PostMeasureLTE
    list_display = ['measdate',
    'district',
    'name',
    'measkt_dl',
    'measkt_ul',
    'measkt_rsrp',
    'measkt_sinr',
    'postmeaskt_dl',
    'postmeaskt_ul',
    'postmeaskt_rsrp',
    'postmeaskt_sinr',
    'postmeasskt_dl',
    'postmeasskt_ul',
    'postmeasskt_rsrp',
    'postmeasskt_sinr',
    'postmeaslg_dl',
    'postmeaslg_ul',
    'postmeaslg_rsrp',
    'postmeaslg_sinr',]
    list_display_links = ['name',]
    search_fields = ('name','measdate') 

class MeasLastyearWeakAdmin(admin.ModelAdmin):
    '''취약지역 작년결과를 위한 클래스'''
    model = MeasLastyearWeak
    list_display = ['measYear','weakmopho',
    'weakvolte',
    'weaktele3g',
    'weaklte',
    'weak3g',]
    list_display_links = ['weakmopho',]
    search_fields = ('weakmopho',) 
# ----------------------------------------------------------------------------------------------------------------------
# 관리자 페이지에 모델을 등록한다.
# ----------------------------------------------------------------------------------------------------------------------
# admin.site.register(MeasPlan, MeasPlanAdmin) # 대상등록 등록
# admin.site.register(MeasLastyear5G, MeasLastyear5GAdmin) # 작년5G 등록
# admin.site.register(MeasLastyearLTE, MeasLastyearLTEAdmin) # 작년LTE 등록
# admin.site.register(MeasLastyearWiFi, MeasLastyearWiFiAdmin) # 작년WiFi 등록
# admin.site.register(MeasLastyeardistrict, MeasLastyeardistrictAdmin) # 작년WiFi 등록
# admin.site.register(MeasLastyearWeak, MeasLastyearWeakAdmin) # 작년품질취약지역 등록
# admin.site.register(LastMeasDayClose, LastMeasDayCloseAdmin) # 작년WiFi 등록
# admin.site.register(ReportMessage, ReportMessageAdmin) # 작년WiFi 등록
# admin.site.register(PostMeasure5G, PostMeasure5GAdmin) # 작년WiFi 등록
# admin.site.register(PostMeasureLTE, PostMeasureLTEAdmin) # 작년WiFi 등록



################################## 별도 관리자 페이지 코드 (22.07.15) #######################################
class ReportAdminSite(admin.AdminSite):
    site_header = "일일보고 관리자 페이지"
    site_title = "일일보고 관리자 페이지"
    index_title = "일일보고 관리자 페이지"
report_admin_site = ReportAdminSite(name='report_admin')

report_admin_site.register(MeasPlan, MeasPlanAdmin) # 대상등록 등록
report_admin_site.register(MeasLastyear5G, MeasLastyear5GAdmin) # 작년5G 등록
report_admin_site.register(MeasLastyearLTE, MeasLastyearLTEAdmin) # 작년LTE 등록
report_admin_site.register(MeasLastyearWiFi, MeasLastyearWiFiAdmin) # 작년WiFi 등록
report_admin_site.register(MeasLastyeardistrict, MeasLastyeardistrictAdmin) # 작년WiFi 등록
report_admin_site.register(MeasLastyearWeak, MeasLastyearWeakAdmin) # 작년품질취약지역 등록
report_admin_site.register(LastMeasDayClose, LastMeasDayCloseAdmin) # 작년WiFi 등록
report_admin_site.register(ReportMessage, ReportMessageAdmin) # 작년WiFi 등록
report_admin_site.register(PostMeasure5G, PostMeasure5GAdmin) # 작년WiFi 등록
report_admin_site.register(PostMeasureLTE, PostMeasureLTEAdmin) # 작년WiFi 등록