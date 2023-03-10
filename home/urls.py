from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [
    path('', views.index, name='index'),  
    path('admin/', views.admin_index, name='admin_index'),  

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
    

]
