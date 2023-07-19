from django.contrib import admin

from agritech import settings
from .models import Category, Project, Tax, ExtraImage,ProjectStatus,Notice
from .models import Cart
from decimal import Decimal

class ExtraImageInline(admin.StackedInline):
    model = ExtraImage
    extra = 1
    max_num = 5  # Set the maximum number of extra images to 5



class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_title', 'display_duration', 'total_no_shares', 'project_type', 'return_date', 'value_of_share', 'percent_return_after_due_date', 'is_approved','is_completed']
    list_editable = ['is_approved']
    search_fields = ['project_title', 'project_type__category_name', 'address']
    

    
    def display_duration(self, obj):
        duration = obj.calculate_duration()
        return f'{duration} months'

    display_duration.short_description = 'Duration'


    class Media:
        if hasattr(settings, 'GOOGLE_API_KEY') and settings.GOOGLE_API_KEY:
            css = {
                'all': ('ecom/css/custom.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?key={}'.format(settings.GOOGLE_API_KEY),
                'ecom/js/location_picker.js',
            )



class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'quantity', 'updated_at')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Category)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectStatus)
admin.site.register(Notice)