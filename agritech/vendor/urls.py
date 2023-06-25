from django.urls import path, include
from . import views
from account import views as AccountViews

urlpatterns = [
    path('', AccountViews.vendordashboard, name='vendor'),
    path('profile/', views.vprofile, name='vprofile'),

    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.productItem_by_category, name='productItem_by_category'),

    # Category CRUD
 
    # path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    # path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # # Prod CRUD
    path('menu-builder/product/add/', views.add_product, name='add_product'),
    path('menu-builder/product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('menu-builder/product/delete/<int:pk>/', views.delete_product, name='delete_product'),

    # path('order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
    path('vendor_order_detail/<int:order_number>/', views.order_detail, name='vendor_order_detail'),
    path('my_orders/', views.my_orders, name='vendor_my_orders'),
    path('active_farms/', views.active_farms, name='active farms'),
    path('vendor/active_farms/<int:project_id>/save_status/', views.save_status, name='save_status'),
    path('farm_status/<int:id>/', views.farm_status, name='farm_status'),
]