from django.contrib import admin
from django.urls import path
from cart import views


urlpatterns = [    
    
    path('', views.cart, name='cart'),        
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),    
    path('remove_cartitems/<int:product_id>/<int:cart_item_id>/', views.remove_cartitems, name='remove_cartitems'),    
    path('remove_cartt/<int:product_id>/<int:cart_item_id>/', views.remove_cartt, name='remove_cartt'),    
 

    path('checkout/', views.checkout, name='checkout'),
    
    path('remove_coupan/', views.remove_coupon, name='remove_coupan'),

    path('success/', views.success, name='success'),    

    path('orderconfirmation/', views.order_confirmation, name='order_confirmation'),
    



]
