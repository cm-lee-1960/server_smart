from django.contrib import admin
from django import forms
from .models import Phone

# class PhoneForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(PhoneForm, self).__init__(*args, **kwargs)
#         # self.fields['phoneGroup'].editable = False
#         self.fields['phoneGroup'].widget.attrs['readonly'] = True
#     class Meta:
#         model = Phone
#         fields = '__all__'
class PhoneAdmin(admin.ModelAdmin):
    # form = PhoneForm
    list_display = ['phone_type', 'phone_no', 'networkId', 'avg_downloadBandwidth', \
        'avg_uploadBandwidth', 'status', 'total_count', 'active']
    list_display_links = ['phone_no']
    search_fields = ('phone_no', )
    list_filter = ['active',]
class MonitorAdminArea(admin.AdminSite):
    index_title = "단말상태 관리"
    site_header = "스마트 상황실 관리"
    site_title = "스마트 상활실"

monitor_site = MonitorAdminArea(name="스마트 상황실")

admin.site.register(Phone, PhoneAdmin)
monitor_site.register(Phone, PhoneAdmin)

