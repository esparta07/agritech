from django.urls import path, include
from . import views

app_name ='account'
from .views import UserRegistrationView, OTPVerificationView
urlpatterns =[
    path('',views.myAccount),
    path('vendor-detail/<int:vendor_id>/', views.vendor_detail, name='vendor_detail'),

    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('verify-otp/', OTPVerificationView.as_view(), name='otp_verification'),
    

    path('login/', views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('myAccount/',views.myAccount, name='myAccount'),
    

    path('custdashboard/',views.custdashboard, name='custdashboard'),
    path('vendordashboard/',views.vendordashboard, name='vendordashboard'),
    path('change_password/', views.change_password, name='change_password'),

    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    
    path('vendor/', include('vendor.urls')),
    path('customer/', include('customers.urls')),
    path('order/', include('orders.urls')),

]