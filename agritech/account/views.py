from django.contrib.auth.tokens import default_token_generator
from django.http.response import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponseRedirect
from ecom.models import Notice
from ecom.models import Project
from orders.models import Order
from django.urls import reverse
from .models import User,UserProfile
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from vendor.models import Vendor
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .forms import UserRegistrationForm
from django.contrib import messages
import random
import requests
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import update_session_auth_hash
import datetime
from django.db.models import Sum, F
from django.utils import timezone
from .forms import CustomPasswordChangeForm


# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


class OTPVerificationView(View):
    def post(self, request):
        submitted_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        password = request.session.get('password')
        role = request.session.get('role')

        if submitted_otp == saved_otp:
            messages.success(request, "OTP verification successful")
            phone_number = request.session.get('phone_number')
            User = get_user_model()
            user = User.objects.create(phone_number=phone_number, role=role)
            user.set_password(password)

            if role == User.VENDOR:
                user.role = User.VENDOR
                user.save()

                # Check if a UserProfile already exists for the user
                user_profile, created = UserProfile.objects.get_or_create(user=user)

                # Create a Vendor object associated with the user and user_profile
                vendor = Vendor.objects.create(
                    user=user,
                    user_profile=user_profile
                )
            else:
                user.role = User.CUSTOMER
                user.save()

            return redirect('account:login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            form = UserRegistrationForm(request.POST)  # Pass the submitted data back to the form
            return render(request, 'account/registration.html', {'form': form, 'otp_required': True, 'password': password})



class UserRegistrationView(View):
    
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'account/registration.html', {'form': form, 'otp_required': False})

    def post(self, request):
        if request.user.is_authenticated:
           messages.warning(request, 'You are already logged in!')
           return HttpResponseRedirect(reverse('account:myAccount'))
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data['phone_number'])

            if 'otp' in request.POST:
                return OTPVerificationView.as_view()(request)
            else:
                password = form.cleaned_data['password']
                otp = generate_otp()
                print(otp)
                
                # Send OTP via SparrowSMS
                send_sms_otp(phone_number, otp)

                request.session['otp'] = otp
                request.session['phone_number'] = phone_number
                request.session['password'] = password
                request.session['role'] = form.cleaned_data['role']
                form.fields['password'].widget.attrs['value'] = password

                return render(request, 'account/registration.html', {'form': form, 'otp_required': True, 'password': password})

        return render(request, 'account/registration.html', {'form': form, 'otp_required': False})



def generate_otp():
    return str(random.randint(100000, 999999))

def send_sms_otp(phone_number, otp):
    extracted_number = phone_number[4:]
    
    url = "http://api.sparrowsms.com/v2/sms/"
    data = {
        'token': 'v2_4Bg0gTIExiCMGTN1GDd9bsUEytF.wHW',
        'from': 'Demo',
        'to': extracted_number,
        'text': f'Your OTP is: {otp}',
    }
    response = requests.post(url, data=data)

    if response.status_code == 200:
        status_code = response.status_code
        response_text = response.text
        response_json = response.json()

        return status_code, response_text

    else:
        return HttpResponse("Error occurred {}".format(response.text))

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('account:myAccount')

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Authenticate using the custom user model
        user = authenticate(request, username=phone_number, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('account:myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('account:login')

    return render(request, 'account/login.html')


#Logout
def logout(request):
   auth.logout(request)
   messages.info(request, 'You are logged out.')
   return redirect('account:login')

@login_required(login_url='account:login')
#Dashboard Assign
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)
    




@login_required(login_url='account:login')
@user_passes_test(check_role_customer)
def custdashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:10]
    
    # Calculate the sum of all amounts of farm orders
    total_investment = orders.aggregate(Sum('farmorder__amount'))['farmorder__amount__sum'] or 0
    return_amount = orders.aggregate(Sum('farmorder__return_amount'))['farmorder__return_amount__sum'] or 0
    
    # Get projects invested by the user with return date within the next 15 days
    today = timezone.now().date()
    return_date_limit = today + timedelta(days=15)
    projects_due_soon = Project.objects.filter(farmorder__order__in=orders, return_date__lte=return_date_limit, return_date__gte=today, farmorder__user=request.user).distinct()
    # Exclude projects where today's date has crossed the return_date
    
    # Get projects invested by the user with the total investment
    invested_projects = Project.objects.filter(farmorder__order__in=orders, farmorder__user=request.user).annotate(total_investment=Sum('farmorder__amount')).annotate(total_quantity=Sum('farmorder__quantity')).annotate(return_amount=Sum('farmorder__return_amount'))
    
    # Calculate the sum of return_amount for completed farm orders
    profit_gained = orders.filter(farmorder__project__is_completed=True).aggregate(total_return_amount=Sum(F('farmorder__return_amount')))['total_return_amount'] or 0
    expected_profit =orders.aggregate(total_return_amount=Sum(F('farmorder__return_amount')))['total_return_amount'] or 0
    
    # Retrieve the relevant notice for customers
    customer_notice = Notice.objects.filter(audience__in=[Notice.USER, Notice.BOTH]).first()

    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_investment': total_investment,
        'return_amount': return_amount,
        'projects_due_soon': projects_due_soon,
        'invested_projects': invested_projects,
        'profit_gained': profit_gained,
        'expected_profit': expected_profit,
        'customer_notice':customer_notice
    }
    return render(request, 'account/custdashboard.html', context)


 
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__user=request.user, is_ordered=True).order_by('created_at')
    recent_orders = orders[:10]

    # Filter current month orders
    current_month = datetime.datetime.now().month
    current_month_orders = Order.objects.filter(vendors__user=request.user, is_ordered=True, created_at__month=current_month)

    # Calculate total revenue
    total_revenue = Order.objects.filter(vendors__user=request.user, is_ordered=True).aggregate(total_revenue=Sum('total'))['total_revenue'] or 0
    project_count = Project.objects.filter(vendor=vendor.user).count()

    projects = Project.objects.filter(vendor=vendor.user,is_approved=True)
    
    # Retrieve the relevant notice for vendors
    vendor_notice = Notice.objects.filter(audience__in=[Notice.VENDOR, Notice.BOTH]).first()
    
    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'show_popup': False,
        'project_count': project_count,
        'projects': projects,
        'vendor_notice':vendor_notice,
        
    }

    if request.user.role == User.VENDOR:
        project = Project.objects.filter(vendor=request.user, return_date__lt=datetime.date.today() + datetime.timedelta(days=15))
        context['project'] = project

        for proj in project:
            remaining_days = (proj.return_date - datetime.date.today()).days
            if remaining_days < 15 and 'modals_hidden' not in request.session:
                context['show_popup'] = True
                request.session['modals_hidden'] = True  # Update session variable

    # Set session expiry
    if request.user.is_authenticated and 'modals_hidden' not in request.session:
        request.session.set_expiry(0)
        request.session['modals_hidden'] = True

    return render(request, 'account/vendordashboard.html', context)




    
    
#Activate User 
def activate(request, uidb64, token):
     # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('account:myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('account:myAccount')
    return

#forgot Password Link
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if UserProfile.objects.filter(email=email).exists():
            user_profile = UserProfile.objects.get(email=email)
            user = user_profile.user

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'account/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('account:login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('account:forgot_password')
    return render(request, 'account/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('account:reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('account:myAccount')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('account:login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('account:reset_password')
    return render(request, 'account/reset_password.html')


@login_required
def customer_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session
            messages.success(request, 'Your password was successfully updated!')
            logout(request)  # Log out the user
            return redirect('index')  
    else:
        form = CustomPasswordChangeForm(user=request.user)  # Pass user=request.user to initialize the form with the user's data
    return render(request, 'account/customer_change_password.html', {'form': form})

@login_required
def vendor_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session
            messages.success(request, 'Your password was successfully updated!')
            logout(request)  # Log out the user
            return redirect('index')  
    else:
        form = CustomPasswordChangeForm(user=request.user)  # Pass user=request.user to initialize the form with the user's data
    return render(request, 'account/vendor_change_password.html', {'form': form})

def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(User, id=vendor_id)
    vendors = Vendor.objects.get(user=vendor)
    user_profile = vendor.userprofile
    project_count = vendor.project_set.count()
    context = {
        'vendor': vendor,
        'user_profile': user_profile,
        'project_count': project_count,
        'vendors': vendors,
    }
    return render(request, 'account/farmer-details.html', context)