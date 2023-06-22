from django import forms
from .models import User , UserProfile
from account.validators import allow_only_images_validator


# UserRegisterations
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'role')



    
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
        
