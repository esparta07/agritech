from django import forms
from .models import User , UserProfile
from account.validators import allow_only_images_validator
from django.utils.safestring import mark_safe

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
            'class': 'custom-class',
            'value': '+977'
        })
        self.fields['phone_number'].label = mark_safe('<label style="font-weight: bold;">Phone Number</label>')
        self.fields['password'].label = mark_safe('<label style="font-weight: bold;">Password</label>')
        self.fields['role'].label = mark_safe('<label style="font-weight: bold; margin-bottom: 5px;">Role</label>')

        # Add wrapper div with styles for each form item
        self.fields['phone_number'].widget = forms.TextInput(attrs={'style': 'width: 100%; max-width: 350px; height: 40px; margin-bottom: 5px; padding: 5px;'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'style': 'width: 100%; max-width: 350px; height: 40px; margin-bottom: 5px; padding: 5px;'})
         # Adjust styles for the radio buttons
        self.fields['role'].widget.attrs.update({
            'style': 'display: inline-block; vertical-align: middle; margin-left: 5px;',
        })

        


    
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
        
