from django.contrib import admin
from .models import Vendor
# Register your models here.


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'created_at')
    
    list_editable = ('is_approved',)
admin.site.register(Vendor,VendorAdmin)