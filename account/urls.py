from django.contrib import admin
from django.urls import path
from account import views


urlpatterns = [
    path('login', views.log_in, name='log_in'),   
    path('logout', views.log_out, name='log_out'),   
    path('signup', views.signup, name='signup'),   
    path('otp', views.signup, name='otp'),
        
]
