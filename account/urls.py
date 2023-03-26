from django.contrib import admin
from django.urls import path
from account import views


urlpatterns = [
    path('login', views.log_in, name='log_in'),   
    path('logout', views.log_out, name='log_out'),   
    path('signup', views.signup, name='signup'), 
    
    # Multiple Address  

    path('addresses', views.view_address, name='addresses'),   
    path('add_address/<int:num>/', views.add_address, name='add_address'),   
    path('addresses/edit_address/<int:id>/<int:num>/', views.edit_address, name='edit_address'),   
    path('addresses/delete_address/<int:id>/<int:nam>/', views.delete_address, name='delete_address'),   
    path('addresses/default_address/<int:id>/<int:new>/', views.default_address, name='default_address'),   
        
]
