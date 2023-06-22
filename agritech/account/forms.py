from django import forms
from .models import User , UserProfile
from account.validators import allow_only_images_validator
from django.utils.safestring import mark_safe

# UserRegisterations
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['phone_number'] = '+977'
        self.fields['phone_number'].widget.attrs.update({
            'class': 'custom-class',
            'style': 'width: 100%; max-width: 470px; height: 53px;',  # Increase the max-width value as desired
            'value': '+977'  # Set the value attribute to '+977'
        })
        self.fields['phone_number'].label = mark_safe('<label style="font-weight: bold;">Phone Number</label>')
        self.fields['password'].label = mark_safe('<label style="font-weight: bold;">Password</label>')
        self.fields['role'].label = mark_safe('<label style="font-weight: bold; margin-top:-40px;">Role</label>')



    
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), required=False)
    cover_photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), required=False)
    
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'passport_photo', 'citizenship_front', 'citizenship_back']




class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['phone_number', 'user_name']
        
