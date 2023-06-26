from django import forms

from account.validators import allow_only_images_validator
from .models import Category, Project
from django.utils.translation import gettext_lazy as _


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']


class ProjectForm(forms.ModelForm):
    farm_image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info w-100'}), validators=[allow_only_images_validator])
    extra_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'btn btn-info w-100', 'multiple': True}), validators=[allow_only_images_validator], required=False)

    return_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    def clean_extra_images(self):
        extra_images = self.cleaned_data.get('extra_images')
        if extra_images and len(extra_images) > 5:
            raise forms.ValidationError(_('Only up to 5 images are allowed.'))

        return extra_images



    class Meta:
        model = Project
        fields = ['project_title', 'project_type', 'project_description', 'total_cost', 'farm_image', 'extra_images', 'is_available',
                   'value_of_share', 'max_shares_per_user', 'return_date', 'percent_return_after_due_date']
