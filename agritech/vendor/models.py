from enum import unique
from django.db import models
from account.models import User, UserProfile
from account.utils import send_notification
from datetime import time, date, datetime

# Create your models here.



class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)

    vendor_name = models.CharField(max_length=50, blank=True)

    vendors_license = models.FileField(upload_to='vendor/license',blank=True, null=True)
    company_registeration = models.FileField(upload_to='vendor/company_registeration',blank=True, null=True)
    vendor_logo=models.FileField(upload_to='vendor/company_logo',blank=True, null=True)
    vendor_description=models.TextField(max_length=500,blank=True, null=True)


    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    

    @property
    def is_vendor_approved(self):
            return self.is_approved
    
    def _str_(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'account/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                if self.user.userprofile.email:
                    context['to_email'] = self.user.userprofile.email
                else:
                    context['to_email'] = ''  # Set a default value if email is not available

                if self.is_approved:
                    # Send notification email
                    mail_subject = "Congratulations! Your restaurant has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)
