
from django.shortcuts import render, get_object_or_404,redirect
from django.http.response import JsonResponse
from django.urls import reverse
from account.models import User
from account.views import check_role_customer
from ecom.models import Category,Project
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required , user_passes_test
from .models import Cart,UserProfile,UserProfile, User, is_project_approved
from .context_processors import get_cart_counter , get_cart_amounts
from orders.forms import OrderForm
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.models import Q


# Create your views here.
def supplier(request):
  
    return render(request, 'ecom/shop.html')





def shop_view(request):
    categories = Category.objects.all()
    projects = Project.objects.filter(is_approved=True,is_soldout=False)  # Filter approved projects
    page = request.GET.get('page')
    search_query = request.GET.get('search_query')
    selected_category = request.GET.get('category')  # Get the selected category from the dropdown
    sort_by = request.GET.get('sort_by')  # Get the value of the 'sort_by' parameter from the request

    if sort_by == 'percent_return':
        projects = projects.order_by('-percent_return_after_due_date')
    elif sort_by == 'duration':
        projects = projects.order_by(F('return_date') - F('created_at'))
    elif sort_by == 'value_of_share':
        projects = projects.order_by('value_of_share')

    if selected_category and selected_category != 'Categories':
        projects = projects.filter(project_type__category_name=selected_category)

    if search_query and search_query.strip() != '':
        project_ids = [project.id for project in projects if
                       project.project_title.lower().find(search_query.lower()) != -1]

        user_profile_ids = [profile.user.id for profile in UserProfile.objects.filter(
            Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
        )]

        vendor_ids = [vendor.id for vendor in User.objects.filter(
            Q(id__in=user_profile_ids) & Q(role=User.VENDOR)
        )]

        projects = projects.filter(Q(id__in=project_ids) | Q(vendor_id__in=vendor_ids))

    paginator = Paginator(projects, 6)
    project_page = paginator.get_page(page)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'project_page': project_page,
        'sort_by': sort_by,
    }

    return render(request, 'ecom/shop-grid.html', context)





@is_project_approved
def prod_view(request, id):
    project = get_object_or_404(Project, id=id)
    
    # Check if the logged-in user is the vendor of the project
    
    top_projects = Project.objects.order_by('-percent_return_after_due_date')[:3]
    related_projects = Project.objects.filter(project_type=project.project_type).exclude(id=project.id)[:5]
    
    if related_projects.count() < 5:
        additional_projects = Project.objects.exclude(id=project.id).annotate(num_projects=Count('id')).order_by('-num_projects')[:5 - related_projects.count()]
        related_projects = list(related_projects) + list(additional_projects)
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    
    context = {
        'project': [project],
        'top_projects': top_projects,
        'related_projects': related_projects,
        'cart_items': cart_items,
    }
    
    return render(request, 'ecom/product-details.html', context)



from django.core.exceptions import ValidationError

@user_passes_test(check_role_customer)
def add_to_cart(request, project_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                project = Project.objects.get(id=project_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, project=project)
                    if chkCart.quantity < project.max_shares_per_user:
                        chkCart.quantity += 1
                        chkCart.save()
                        return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                    else:
                        return JsonResponse({'status': 'Failed', 'message': 'Maximum share limit reached '})
                except Cart.DoesNotExist:
                    if project.max_shares_per_user > 0:
                        if project.total_no_shares > 0:
                            chkCart = Cart.objects.create(user=request.user, project=project, quantity=1)
                            return JsonResponse({'status': 'Success', 'message': 'Added the project to the cart', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                        else:
                            return JsonResponse({'status': 'Failed', 'message': 'No more shares available for this project!'})
                    else:
                        return JsonResponse({'status': 'Failed', 'message': 'Maximum share limit reached'})
            except Project.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This project does not exist!'})
            except ValidationError as e:
                error_message = ' '.join(e.messages)
                return JsonResponse({'status': 'Failed', 'message': error_message})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})








def decrease_cart(request, project_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the project exists
            try:
                project = Project.objects.get(id=project_id)
                # Check if the user has already added that project to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user, project=project)
                    if chkCart.quantity > 1:
                        # decrease the cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity,'cart_amount': get_cart_amounts(request), })
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
        
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})



def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request),'cart_amount': get_cart_amounts(request)})

            except Cart.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})
    
@user_passes_test(check_role_customer)
@login_required(login_url = 'account:login')
def cart_view(request):
    
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'ecom/cart.html', context)



@user_passes_test(check_role_customer)
@login_required(login_url='account:login')
def checkout_view(request):
    
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('ecom:shop')
    
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'phone': request.user.phone_number,
        'email': user_profile.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request,'ecom/checkout.html',context )


