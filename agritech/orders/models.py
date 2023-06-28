import json
from django.db import models
from account.models import User
from orders import request_object
from ecom.models import Project
from vendor.models import Vendor
from decimal import Decimal

# Create your models here.
import logging
class Payment(models.Model):
  
  pidx = models.CharField(max_length=200)
  payment_status = models.JSONField(null=True, blank=True)

  def __str__(self):
        return self.pidx
    
    
class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True)

    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=25, blank=True)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10,blank=True)

    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text = "Data format: {'tax_type':{'tax_percentage':'tax_amount'}}")
    total_tax = models.FloatField()
    total_data = models.JSONField(blank=True, null=True)

    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def order_placed_to(self):
        return ", ".join([vendor.vendor_name for vendor in self.vendors.all()])
    
    def __str__(self):
        return f"Order {self.order_number} - Placed to: {self.order_placed_to()}"

    def get_total_by_vendor(self, vendor):
        subtotal = 0
        tax = 0
        tax_dict = {}

        if self.total_data:
            tax_data = json.loads(self.tax_data)
            data = tax_data.get(str(vendor.id))

            for key, val in data.items():
                val_float = float(val)  # Convert val to float
                subtotal += val_float
                val = val.replace("'", '"')
                val = json.loads(val)
                tax_dict.update(val)

                # Calculate tax
                # {'CGST': {'9.00': '6.03'}, 'SGST': {'7.00': '4.69'}}
                for i in val:
                    for j in val[i]:
                        tax += float(val[i][j])

        grand_total = subtotal + tax  # No need to convert to float again
        context = {
            'subtotal': subtotal,
            'tax_dict': tax_dict,
            'grand_total': grand_total,
        }

        # Debug output
        logging.debug("subtotal: %s", subtotal)
        logging.debug("tax_dict: %s", tax_dict)
        logging.debug("grand_total: %s", grand_total)

        return context

    def __str__(self):
        vendor_names = ', '.join([vendor.vendor_name or f"{vendor.user.userprofile.first_name} {vendor.user.userprofile.last_name}" for vendor in self.vendors.all()])
        if vendor_names:
            return f"Order {self.order_number} - Placed to: {vendor_names}"
        else:
            return f"Order {self.order_number} - Placed by: {self.user.userprofile.first_name} {self.user.userprofile.last_name}"

 
class FarmOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    
    return_amount = models.FloatField(default=0)
    reservation_expiration = models.DateTimeField(null=True, blank=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def order_placed_to(self):
        return ", ".join([vendor.vendor_name for vendor in self.vendors.all()])

    def __str__(self):
        return self.project.project_title
    
    def update_return_amount(self):
        percent_return = self.project.percent_return_after_due_date / Decimal('100')
        self.return_amount = round(percent_return * Decimal(str(self.amount)), 2)
        self.save()


    
