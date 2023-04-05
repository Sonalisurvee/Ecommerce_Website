from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [
    path('', views.index, name='index'),  
    path('admin/sales', views.sales, name='sales'),  

    #user profile

    path('profile/', views.profile, name="profile"),  
    path('update_profile/<int:user_id>', views.update_profile, name="update_profile"), 

    #order listing in user side
    
    path('profile/orders-list/', views.orders_list, name="orders_list"),
    path('profile/orders-list/order-details/<str:order_id>/', views.order_details, name="order_details"),
    path('profile/orders-list/order-details/order-tracking/<int:item_id>/', views.order_tracking, name="tracking"),
    path('profile/orders-list/order-invoice/<str:order_id>/', views.order_invoice, name="order_invoice"),
    path('profile/orders-list/order-details/cancel-order/<int:item_id>/<str:order_id>', views.cancel_order, name="cancel_order"),

    #banner management
    
    path('admin/banner_management', views.banner_management, name='banner_management'),       
    path('admin/banner_management/banner_delete/<int:banner_id>/', views.banner_delete, name='banner_delete'),       
    path('admin/banner_management/banner_edit/<int:banner_id>/', views.banner_edit, name='banner_edit'),  
    path('admin/banner_management/delet_image/<int:carousel_id>/', views.delet_image, name='delet_image'),  
 
     # Variants management

    path('admin/variant_management', views.variant_management, name='variant_management'),       
    path('admin/variant_management/variant_delete/<int:id>/', views.variant_delete, name='variant_delete'),       
    path('admin/variant_management/variant_edit/<int:id>/', views.variant_edit, name='variant_edit'), 
    path('admin/variant_management/add_variant/', views.add_variant, name='add_variant'), 

    # about

    path('about/', views.about, name='about'),  


]
