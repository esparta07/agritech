from django import forms
from .models import Vendor
from django.core.validators import FileExtensionValidator
from account.validators import allow_only_images_validator


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


