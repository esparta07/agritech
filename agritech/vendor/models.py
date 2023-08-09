from enum import unique
from django.db import models
from account.models import User, UserProfile
from account.utils import send_notification
from datetime import time, date, datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(
        User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(
        UserProfile, related_name='userprofile', on_delete=models.CASCADE)

    vendor_name = models.CharField(max_length=50, blank=True)

    vendors_license = models.FileField(
        upload_to='vendor/license', blank=True, null=True)
    company_registeration = models.FileField(
        upload_to='vendor/company_registeration', blank=True, null=True)
    vendor_logo = models.FileField(
        upload_to='vendor/company_logo', blank=True, null=True)
    vendor_description = models.TextField(
        max_length=500, blank=True, null=True)

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def is_vendor_approved(self):
        return self.is_approved

    def __str__(self):
        return self.vendor_name

    
