from urllib import response
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from account.views import check_role_customer
from ecom.models import Cart, Tax
from ecom.context_processors import get_cart_amounts
from ecom.models import Project
from .forms import OrderForm
from .models import Order, FarmOrder, Payment
import json
from .utils import generate_order_number, order_total_by_vendor
from account.utils import send_notification
from django.contrib.auth.decorators import login_required , user_passes_test
import requests
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import F


 

# from productOnline_main.settings import RZP_KEY_ID, RZP_KEY_SECRET
from django.contrib.sites.shortcuts import get_current_site


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('ecom:shop')
    
    vendors_user_ids = []
    for i in cart_items:
        if i.project.vendor.user.id not in vendors_user_ids:
            vendors_user_ids.append(i.project.vendor.user.id)

    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    
    if request.method == 'POST':
        

        form = OrderForm(request.POST)
        if form.is_valid():
            print("POST Data:")
            for key, value in request.POST.items():
                print(f"{key}: {value}")
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            
            # Remove country code and keep the last 10 digits of the phone number
            phone_number = form.cleaned_data['phone']
            phone_number = phone_number[-10:]
            form.cleaned_data['phone'] = phone_number
            order.phone=phone_number
            for cart_item in cart_items:
                order.project = cart_item.project
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data, cls=DjangoJSONEncoder)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save()
            order_number = generate_order_number(order.id)
            order.order_number = order_number
            order.vendors.set(vendors_user_ids)
            order.save()

            
            # Store the modified order form data and order number in the session
            request.session['order_form_data'] = form.cleaned_data
            request.session['order_number'] = order_number
            
            # Print session data in the terminal
            print("Session Data:", request.session['order_form_data'])
            print("Order Number:", request.session['order_number'])
           
            form = OrderForm()
            context = {
                'order': order,
                'form': form,
                'cart_items': cart_items
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)

    return render(request, 'orders/place_order.html')




@login_required(login_url='login')
@user_passes_test(check_role_customer)
def payments(request):
    order_form_data = request.session.get('order_form_data')
    order_number = request.session.get('order_number')
    subtotal = get_cart_amounts(request)['subtotal']
    grand_total = get_cart_amounts(request)['grand_total']

    if order_form_data:
        order = Order.objects.get(user=request.user, order_number=order_number)
        data = {
            "return_url": "http://127.0.0.1:8000/orders/verify",
            "website_url": "http://127.0.0.1:8000/",
            "amount": int(grand_total * 100),
            "purchase_order_id": order_number,
            "purchase_order_name": "test1",
            "customer_info": {
                "name": order_form_data['first_name'] + ' ' + order_form_data['last_name'],
                "email": order_form_data['email'],
                "phone": order_form_data['phone'],
            },
        }

        headers = {
            "Authorization": "Key ca62b8971c65497d949f5ba938b58c09"
        }

        response = requests.post("https://a.khalti.com/api/v2/epayment/initiate/", json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            pidx = data.get("pidx")
            payment = Payment(pidx=pidx)

            payment.save()
            order.payment = payment
            order.is_ordered = True
            order.save()

            cart_items = Cart.objects.filter(user=request.user)
            collected_amount = subtotal 
            for item in cart_items:
                ordered_product = FarmOrder()
                ordered_product.order = order
                ordered_product.payment = payment
                ordered_product.user = request.user
                ordered_product.project = item.project
                ordered_product.quantity = item.quantity
                ordered_product.price = item.project.value_of_share
                ordered_product.amount = item.project.value_of_share * item.quantity
                ordered_product.update_return_amount()
                ordered_product.save()

                Project.objects.filter(pk=item.project.pk).update(
                    total_no_shares=F('total_no_shares') - item.quantity,
                    collected_amount=F('collected_amount') + collected_amount,
                )

                project = Project.objects.get(pk=item.project.pk)
                if project.total_no_shares == 0:
                    project.is_soldout = True
                    project.save()
 

            return HttpResponseRedirect(data.get("payment_url"))

    return render(request, 'orders/pay_error.html')


def verify(request):
    pidx = request.GET.get('pidx')
    
    
    data = {
        "pidx": pidx
    }
    headers = {
        "Authorization": "Key ca62b8971c65497d949f5ba938b58c09"  
    }
    response = requests.post("https://a.khalti.com/api/v2/epayment/lookup/", json=data, headers=headers)
    data = response.json()
    status = data.get("status")
    updated_pidx = data.get("pidx")

    status_details = {
        "status": status,
        "pidx": updated_pidx
    }

    payment_status_object = Payment(payment_status=status_details)
    payment_status_object.save()

    # Retrieve the associated order using the purchase_order_id from the query parameters
    order_number = request.GET.get('purchase_order_id')
    order = Order.objects.get(order_number=order_number)

    # Delete cart items
    Cart.objects.filter(user=request.user).delete()

    return redirect('order_complete', order_id=order.id)


@login_required(login_url='account:login')
def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    tax_data = json.loads(order.tax_data)
    subtotal = order.total - calculate_tax_total(tax_data)
    
    # Retrieve the FarmOrder objects associated with the order
    farm_orders = FarmOrder.objects.filter(order=order)

    context = {
        'order': order,
        'subtotal': subtotal,
        'tax_data': tax_data,
        'farm_orders': farm_orders,  # Pass the farm_orders to the context
    }

    return render(request, 'orders/order_complete.html', context)


def calculate_tax_total(tax_data):
    tax_total = 0
    for tax_type, tax_values in tax_data.items():
        for percentage, tax_amount in tax_values.items():
            tax_total += float(tax_amount)
    return tax_total




    




