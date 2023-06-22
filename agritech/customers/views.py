from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from account.forms import UserInfoForm, UserProfileForm
from account.models import UserProfile
from django.contrib import messages
from orders.models import Order, FarmOrder

import simplejson as json


@login_required(login_url='login')
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        
        print(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if profile_form.is_valid() :
            profile_form.save()
            
            messages.success(request, 'Profile updated')
            return redirect('account:cprofile')
        else:
            print(profile_form.errors)
            
    else:
       
        profile_form = UserProfileForm(instance=profile)
        

    context = {
        'profile_form': profile_form,
        'profile': profile,
    }
    return render(request, 'customers/cprofile.html', context)


def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'customers/my_orders.html', context)





def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_product = FarmOrder.objects.filter(order=order)
        subtotal = 0
        for item in ordered_product:
            subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data) if order.tax_data else {}
        context = {
            'order': order,
            'ordered_product': ordered_product,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }
    except json.JSONDecodeError as e:
        print(f"Error decoding tax_data: {str(e)}")
    
    return render(request, 'customers/order_detail.html', context)

    
    
    