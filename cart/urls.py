from django.contrib import admin
from django.urls import path
from cart import views


urlpatterns = [    
    
    path('', views.cart, name='cart'),        
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
      

    path('checkout/', views.checkout, name='checkout'),
    
    path('remove_coupan/', views.remove_coupon, name='remove_coupan'),

    path('success/', views.success, name='success'),    

    # after ajax
    path('delete',views.cart_delete,name="cart-delete"),

    path('update',views.cart_update,name="cart-update"),



]

# this is my private project