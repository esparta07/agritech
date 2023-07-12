from django import forms

from account.validators import allow_only_images_validator
from .models import Category, ExtraImage, Project ,ProjectStatus
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
from django.forms import formset_factory


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']



class ProjectForm(forms.ModelForm):
    project_title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    farm_image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        required=False
    )
    return_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    extra_images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'multiple': True}),
        required=False
    )
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_available', 'is_approved', 'is_completed', 'is_soldout' , 'description']:
                field.widget.attrs.update({'class': 'form-control'})


    class Meta:
        model = Project
        fields = ['project_title', 'project_type', 'project_description', 'project_documents', 'total_cost', 'farm_image', 'is_available',
                  'value_of_share', 'max_shares_per_user', 'return_date', 'percent_return_after_due_date', 'extra_images',
                  'address', 'latitude' , 'longitude']
        exclude = ['is_approved', 'is_completed', 'is_soldout']



ExtraImageFormSet = formset_factory(ProjectForm, extra=1, can_delete=True)


class EditProjectForm(forms.ModelForm):
    
    farm_image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        required=False
    )
    
    extra_images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'multiple': True}),
        required=False
    )

    project_document = forms.FileField(required=False)
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_available', 'is_approved', 'is_completed', 'is_soldout']:
                field.widget.attrs.update({'class': 'form-control'})


    class Meta:
        model = Project
        fields = [ 'project_description','farm_image','project_documents',
                    'extra_images']
        exclude = ['is_approved', 'is_completed', 'is_soldout']
