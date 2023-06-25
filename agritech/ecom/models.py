from tabnanny import verbose
from django.db import models
from django.shortcuts import get_object_or_404
from vendor.models import Vendor
from django.utils import timezone
from account.models import UserProfile ,User
from vendor.models import Vendor
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseForbidden


class Category(models.Model):
    
    category_name = models.CharField(max_length=50)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def clean(self):
        self.category_name = self.category_name.capitalize()
        existing_categories = Category.objects.filter(category_name=self.category_name)
        if self.pk:
            existing_categories = existing_categories.exclude(pk=self.pk)
        if existing_categories.exists():
            raise ValidationError(f"{self.category_name} already exists as a category.")

    def __str__(self):
        return self.category_name



class Project(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': User.VENDOR} ) # Limit choices to vendor users
    project_title = models.CharField(max_length=100)
    project_type = models.ForeignKey(Category, on_delete=models.CASCADE)
    project_description = models.TextField(max_length=500)
    
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_no_shares = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    collected_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    
    value_of_share = models.DecimalField(max_digits=10, decimal_places=2)
    max_shares_per_user = models.PositiveIntegerField()
    return_date = models.DateField()
    percent_return_after_due_date = models.DecimalField(max_digits=5, decimal_places=2)
    
    farm_image = models.ImageField(upload_to='media/farmimages/', default='', blank=True)
    descrption_title = models.CharField(max_length=100,blank=True)
    

    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_completed= models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def fund_invested(self):
        total_cost_decimal = Decimal(self.total_cost)
        return total_cost_decimal * Decimal('0.6')

    @property
    def demand(self):
        return self.total_cost - self.fund_invested
    
    def amount_left(self):
        return self.demand-self.collected_amount

    def num_shares_available(self):
        value_of_share_decimal = float(self.value_of_share)
        demand_decimal = float(self.demand)
        num_shares = round(demand_decimal / value_of_share_decimal)
        self.total_no_shares = num_shares  # Save the value to the field
        self.save()  # Save the model instance
        return num_shares

    def calculate_duration(self):
        duration = self.return_date.month - self.created_at.month
        if self.return_date.year > self.created_at.year:
            duration += 12 * (self.return_date.year - self.created_at.year)
        return duration
    
    def days_since_created(self):
        today = timezone.now().date()
        created_date = self.created_at.date()
        days = (today - created_date).days
        return days
    
    @property
    def duration_in_months(self):
       start_date = self.created_at.date()
       return_date = self.return_date
       duration = return_date.year * 12 + return_date.month - (start_date.year * 12 + start_date.month)
       return duration
    
    def __str__(self):
        return f"{self.pk} - Shares Available: {self.num_shares_available}"
    @property
    def vendor_username(self):
        return self.vendor.username

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def __str__(self):
        return self.project_title
    
    def save(self, *args, **kwargs):
        self.project_title = self.project_title.title()
        super(Project, self).save(*args, **kwargs)

def is_project_approved(view_func):
    def wrapper(request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs['id'])
        if not project.is_approved:
            return HttpResponseForbidden("Project is not approved.")
        return view_func(request, *args, **kwargs)
    return wrapper

    
def validate_extra_images_count(value):
    if value.count() > 5:
        raise ValidationError(_('Only up to 5 extra images are allowed.'))

class ExtraImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='extra_images/')

    def clean(self):
        validate_extra_images_count(self.project.extra_images.exclude(pk=self.pk))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class ProjectStatus(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='statuses')
    title = models.CharField(max_length=100 ,default='Status Update',blank=True,null=True)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Status '{self.status}' for Project '{self.project.project_title}'"

    class Meta:
        verbose_name = 'project status'
        verbose_name_plural = 'project statuses'



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        max_shares_per_user = self.project.max_shares_per_user
        total_shares = self.project.total_no_shares
        # Check if the quantity exceeds the maximum shares per user
        if self.quantity > max_shares_per_user:
            raise ValidationError("Quantity exceeds the maximum shares per user")
        if self.quantity > total_shares:
            raise ValidationError("Quantity exceeds the available shares")
        super().save(*args, **kwargs)

    def clean(self):
        max_shares_per_user = self.project.max_shares_per_user
        total_shares = self.project.total_no_shares
        # Check if the quantity exceeds the maximum shares per user
        if self.quantity > max_shares_per_user:
            raise ValidationError("Quantity exceeds the maximum shares per user")
        # Check if the quantity exceeds the available shares
        if self.quantity > total_shares:
            raise ValidationError("Quantity exceeds the available shares")

    def __str__(self):
        return str(self.user)



class Tax(models.Model):
    tax_type = models.CharField(max_length=20, unique=True)
    tax_percentage = models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Tax Percentage (%)')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'tax'

    def __str__(self):
        return self.tax_type

class MyImage(models.Model):
    image = models.ImageField(upload_to='images/')
    # other fields as needed