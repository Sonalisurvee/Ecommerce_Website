from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [
    path('', views.index, name='index'),  
    path('admin/', views.admin_index, name='admin_index'),  

    # coupon management

    path('admin/coupan_management', views.coupan_management, name='coupan_management'),  
    path('admin/delete_coupon/<int:coupan_id>', views.delete_coupon, name='delete_coupon'),
    path('admin/update_coupon/<int:coupan_id>/', views.update_coupon, name='update_coupon'),
    path('admin/expired/<int:coupan_id>/', views.expired, name='expired'),
    path('admin/add_coupon', views.add_coupon, name='add_coupon'),
   

    #user profile

    path('profile/', views.profile, name="profile"),  
    path('update_profile/<int:user_id>', views.update_profile, name="update_profile"), 

    #user management

    path('user_management', views.user_management, name='user_management'),  
    path('block_unblock/<int:user_id>', views.block_unblock, name='block_unblock'), 

    #banner management
    
    path('banner_management', views.banner_management, name='banner_management'),       
    path('banner_delete/<int:banner_id>/', views.banner_delete, name='banner_delete'),       
    path('banner_edit/<int:banner_id>/', views.banner_edit, name='banner_edit'),  
    
    # order management

    path('order_management/', views.order_management, name='order_management'),       

    path('order_management/<int:order_id>/', views.order_management, name='order_management'),       
    
    
    
    # path('orders/', views.orders, name="orders"),  



]
