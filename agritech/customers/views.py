
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from account.forms import UserProfileForm
from account.models import UserProfile
from django.contrib import messages
from orders.models import Order, FarmOrder
from account.models import User
from ecom.models import Project
import json
from ecom.models import ProjectStatus
from django.db.models import Sum

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

    
def my_investment(request, customer_id):
    # Assuming customer_id is the ID of the customer user

    # Retrieve the customer user object
    customer = User.objects.get(id=customer_id, role=User.CUSTOMER)

    # Retrieve the ordered projects by the customer
    ordered_projects = Project.objects.filter(farmorder__user=customer).distinct()

    # Create a dictionary to store project details, quantity, and price paid
    project_details = {}

    # Iterate over the ordered projects
    for project in ordered_projects:
        # Retrieve the FarmOrder objects for the project and customer
        farm_orders = FarmOrder.objects.filter(user=customer, project=project)

        # Initialize variables to store the total quantity and price paid for the project
        total_quantity = 0
        # total_price_paid = 0

        # Iterate over the FarmOrder objects
        for farm_order in farm_orders:
            # Get the quantity and price paid for each FarmOrder
            quantity_ordered = farm_order.quantity
            # price_paid = farm_order.amount

            # Increment the total quantity and price paid
            total_quantity += quantity_ordered
            # total_price_paid += price_paid

        # Store the project details, total quantity, and total price paid in the dictionary
        project_details[project] = {
            'quantity_ordered': total_quantity,
            # 'price_paid': total_price_paid,
        }

    # Pass the project details dictionary to the template
    return render(request, 'customers/my_investment.html', {'project_details': project_details})

@login_required(login_url='account:login')
def cfarm_status(request, id):
    project = get_object_or_404(Project, id=id)
    
    # Retrieve the status messages for the specific project ID
    status_messages = ProjectStatus.objects.filter(project_id=id).order_by('created_at')
    
    # Calculate the invested amount for the current user and project
    invested_amount = FarmOrder.objects.filter(project=project, user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate the return amount for the current user and project
    return_amount = FarmOrder.objects.filter(project=project, user=request.user).aggregate(Sum('return_amount'))['return_amount__sum'] or 0
    
    context = {
        'project': [project],
        'status_messages': status_messages,
        'invested_amount': invested_amount,
        'return_amount': return_amount,
    }
    
    return render(request, 'customers/cfarm_status.html', context)

