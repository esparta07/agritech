from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
 
app_name ='ecom'

urlpatterns =[
    path('supplier/',views.supplier, name='supplier'),
    path('' , views.shop_view,name='shop'),
    path('<int:id>/', views.prod_view, name='product'),
     # ADD TO CART
    path('add_to_cart/<int:project_id>/', views.add_to_cart, name='add_to_cart'),
    # DECREASE CART
    path('decrease_cart/<int:project_id>/', views.decrease_cart, name='decrease_cart'),
    # DELETE CART ITEM
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),
    path('cart/', views.cart_view,name='cart'),
    
    path('checkout/', views.checkout_view,name='checkout')
   
]