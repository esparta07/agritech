from django import template
from vendor.models import Project

register = template.Library()

@register.filter
def get_project_count(category, vendor):
    return Project.objects.filter(vendor=vendor, project_type=category).count()
