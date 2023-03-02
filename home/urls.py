from django.contrib import admin
from django.urls import path
from home import views


urlpatterns = [
    path('', views.index, name='index'),  
    path('admin/', views.admin_index, name='admin_index'),  
    path('admin/', views.admin_index, name='admin_'),  
    path('profile', views.profile, name="profile"),  
    path('block_unblock/<int:user_id>/', views.block_unblock, name='block_unblock'),       
]
