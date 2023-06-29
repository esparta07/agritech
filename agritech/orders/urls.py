from django.urls import path
from . import views


urlpatterns = [
   
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('verify/', views.verify , name='verify'),
    path('order/<int:order_id>/', views.order_complete, name='order_complete'),

]