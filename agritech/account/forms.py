from django import forms
from .models import User , UserProfile
from account.validators import allow_only_images_validator
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import PasswordChangeForm

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'radio-inline'})
    )

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['phone_number'] = '+977'
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'value': '+977',
            'placeholder': 'Phone Number'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'

        })
     
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), required=False)
   
    
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'profile_picture', 'email' , 'gender' , 'address', 'country', 'state', 'city', 'pin_code', 'passport_photo', 'citizenship_front', 'citizenship_back' ,
                  'facebook', 'linkedin' , 'twitter' , 'instagram']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

            

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'user_name']
        


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add form control attributes to the fields
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})