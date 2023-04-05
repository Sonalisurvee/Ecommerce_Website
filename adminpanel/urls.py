from django.contrib import admin
from django.urls import path
from adminpanel import views


urlpatterns = [
    
    # coupon management

    path('coupan_management', views.coupan_management, name='coupan_management'),  
    path('delete_coupon/<int:coupan_id>', views.delete_coupon, name='delete_coupon'),
    path('update_coupon/<int:coupan_id>/', views.update_coupon, name='update_coupon'),
    path('expired/<int:coupan_id>/', views.expired, name='expired'),
    path('add_coupon', views.add_coupon, name='add_coupon'),  
    
    #user management

    path('admin/user_management', views.user_management, name='user_management'),  
    path('admin/block_unblock/<int:user_id>', views.block_unblock, name='block_unblock'), 

    # order management

    path('admin/order_management/', views.order_management, name='order_management'),
    path('admin/order_management/order_details/<int:id>/', views.view_order, name='view_order'),       
    path('admin/order_management/order_details/update_status/<int:id>/', views.update_status, name='update_status'),       
    
    # Review management

    path('admin/review_management/', views.review_management, name='review_management'),
    path('admin/review_management/delete_review/<int:id>', views.delete_review, name='delete_review'),    

    # admin profile

    path('admin/profile/', views.admin_profile, name='admin_profile'),       
    path('admin/profile/admin_profile_update/<int:admin_id>', views.admin_profile_update, name='admin_profile_update'),       

]
