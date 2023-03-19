from django.contrib import admin
from django.urls import path
from cart import views


urlpatterns = [
    path('', views.cart, name='cart'),    
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),    
    path('remove_cartitem/<int:product_id>/<int:cart_item_id>/', views.remove_cartitem, name='remove_cartitem'),    
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),    

    path('checkout/', views.checkout, name='checkout'),
    # path('order_success/', views.order_success, name='order_success'),
    
    path('remove_coupan/<int:cart_id>/', views.remove_coupan, name='remove_coupan'),
         
    path('placeorder/', views.placeorder, name='placeorder'),
    path('orderconfirmation/', views.order_confirmation, name='order_confirmation'),


]
