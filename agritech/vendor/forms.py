from django import forms

from orders.models import FarmOrder
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ProjectStatusForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ProjectStatus
        fields = ['title', 'status']




