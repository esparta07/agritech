from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

import datetime

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        # Create and save a new user with the given phone number and password
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        # Create and save a new superuser with the given phone number and password
        user = self.create_user(phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICES = (
        (VENDOR, 'Farmer'),
        (CUSTOMER, 'Investor'),
    )
    user_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=False, default="")

    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)

    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    tole_no = models.CharField(max_length=15, blank=True, null=True)

    passport_photo = models.ImageField(upload_to='users/passport_photo', blank=True, null=True)
    citizenship_front = models.ImageField(upload_to='users/citicenship_photo', blank=True, null=True)
    citizenship_back = models.ImageField(upload_to='users/citicenship_photo', blank=True, null=True)

    facebook = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.phone_number)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile
from vendor.models import Vendor

@receiver(post_save, sender=User)
def post_save_create_profile_vendor_receiver(sender, instance, created, **kwargs):
    if created:
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        print('User profile is created')

        if instance.role == User.VENDOR:
            vendor = Vendor.objects.create(user=instance, user_profile=profile)
            print('Vendor is created:', vendor)

    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print('User profile is updated')

        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=instance)
            print('User profile does not exist, created')

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
