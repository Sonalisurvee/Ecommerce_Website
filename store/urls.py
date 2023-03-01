from django.contrib import admin
from django.urls import path
from store import views


urlpatterns = [
    path('', views.product_management, name="product_management"),   
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('update_product/<int:product_id>/', views.update_product, name='update_product'),  
    path('add_product', views.add_product, name='add_product'),
    path('product_list', views.product_list, name='product_list'),

]
 