from django.contrib import admin
from .models import Phone
# from .forms import PhoneAdminForm

# Register your models here.
@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['phone_type', 'phone_no', 'networkId', 'avg_downloadBandwidth', \
        'avg_uploadBandwidth', 'status', 'total_count', 'active']
    list_display_links = ['phone_no']
    search_fields = ('phone_no', )
    list_filter = ['active',]