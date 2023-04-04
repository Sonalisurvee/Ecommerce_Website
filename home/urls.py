from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [
    path('', views.index, name='index'),  
    path('admin/sales', views.sales, name='sales'),  

    # coupon management

    path('admin/coupan_management', views.coupan_management, name='coupan_management'),  
    path('admin/delete_coupon/<int:coupan_id>', views.delete_coupon, name='delete_coupon'),
    path('admin/update_coupon/<int:coupan_id>/', views.update_coupon, name='update_coupon'),
    path('admin/expired/<int:coupan_id>/', views.expired, name='expired'),
    path('admin/add_coupon', views.add_coupon, name='add_coupon'),   

    #user profile

    path('profile/', views.profile, name="profile"),  
    path('update_profile/<int:user_id>', views.update_profile, name="update_profile"), 

    #order listign in user side
    
    path('profile/orders-list/', views.orders_list, name="orders_list"),
    path('profile/orders-list/order-details/<str:order_id>/', views.order_details, name="order_details"),
    path('profile/orders-list/order-details/order-tracking/<int:item_id>/', views.order_tracking, name="tracking"),
    path('profile/orders-list/order-invoice/<str:order_id>/', views.order_invoice, name="order_invoice"),
    path('cancel-order/<int:item_id>/<str:order_id>', views.cancel_order, name="cancel_order"),

    #user management

    path('admin/user_management', views.user_management, name='user_management'),  
    path('admin/block_unblock/<int:user_id>', views.block_unblock, name='block_unblock'), 

    #banner management
    
    path('admin/banner_management', views.banner_management, name='banner_management'),       
    path('admin/banner_management/banner_delete/<int:banner_id>/', views.banner_delete, name='banner_delete'),       
    path('admin/banner_management/banner_edit/<int:banner_id>/', views.banner_edit, name='banner_edit'),  
    path('admin/banner_management/delet_image/<int:carousel_id>/', views.delet_image, name='delet_image'),  
    
    # order management

    path('admin/order_management/', views.order_management, name='order_management'),
    path('admin/order_management/order_details/<int:id>/', views.view_order, name='view_order'),       
    path('admin/order_management/order_details/update_status/<int:id>/', views.update_status, name='update_status'),       
    
    # Review management

    path('admin/review_management/', views.review_management, name='review_management'),
    path('admin/review_management/delete_review/<int:id>', views.delete_review, name='delete_review'),    

    # Variants management

    path('admin/variant_management', views.variant_management, name='variant_management'),       
    path('admin/variant_management/variant_delete/<int:id>/', views.variant_delete, name='variant_delete'),       
    path('admin/variant_management/variant_edit/<int:id>/', views.variant_edit, name='variant_edit'), 
    path('admin/variant_management/add_variant/', views.add_variant, name='add_variant'), 


    # admin profile

    path('admin/profile/', views.admin_profile, name='admin_profile'),       
    path('admin/profile/admin_profile_update/<int:admin_id>', views.admin_profile_update, name='admin_profile_update'),       

    # about

    path('about/', views.about, name='about'),  


]
