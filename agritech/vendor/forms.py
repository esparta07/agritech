from django import forms
from .models import Vendor
from django.core.validators import FileExtensionValidator
from account.validators import allow_only_images_validator
from ecom.models import ProjectStatus

class VendorForm(forms.ModelForm):
    vendor_logo = forms.ImageField(
        label='Vendor Logo',
        required=False,
        widget=forms.FileInput(attrs={'class': 'attach-button'}),
        validators=[allow_only_images_validator],
    )
    company_registeration = forms.FileField(
        label='Company Registration',
        required=False,
        widget=forms.FileInput(attrs={'class': 'attach-button'}),
        validators=[allow_only_images_validator],
    )

    class Meta:
        model = Vendor
        fields = ['vendor_logo', 'company_registeration','vendor_description']

class ProjectStatusForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ProjectStatus
        fields = ['title', 'status']



