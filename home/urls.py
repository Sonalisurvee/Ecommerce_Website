from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [
    path('', views.index, name='index'),  
    path('admin/', views.admin_index, name='admin_index'),  

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

    # path('profile/order_list/', views.order_list, name="order_list"), 
    # path('profile/order_details/', views.order_details, name="order_details"), 

    
    path('profile/orders-list/', views.orders_list, name="orders_list"),

    path('profile/order-details/<str:order_id>/', views.order_details, name="order_details"),

    path('profile/order-tracking/<int:item_id>/', views.order_tracking, name="tracking"),
    path('order-invoice/<str:order_id>/', views.order_invoice, name="order_invoice"),
    path('cancel-order/<int:item_id>/<str:order_id>', views.cancel_order, name="cancel_order"),


    #user management

    path('user_management', views.user_management, name='user_management'),  
    path('block_unblock/<int:user_id>', views.block_unblock, name='block_unblock'), 

    #banner management
    
    path('banner_management', views.banner_management, name='banner_management'),       
    path('banner_management/banner_delete/<int:banner_id>/', views.banner_delete, name='banner_delete'),       
    path('banner_management/banner_edit/<int:banner_id>/', views.banner_edit, name='banner_edit'),  
    path('banner_management/delet_image/<int:carousel_id>/', views.delet_image, name='delet_image'),  
    
    # order management

    path('admin/order_management/', views.order_management, name='order_management'),
    path('admin/order_details/<int:id>/', views.view_order, name='view_order'),       
    path('admin/update_status/<int:id>/', views.update_status, name='update_status'),       
    
    
    
    # path('orders/', views.orders, name="orders"),  



]
