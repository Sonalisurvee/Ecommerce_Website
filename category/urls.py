from django.contrib import admin
from django.urls import path
from category import views


urlpatterns = [
    path('', views.category_management, name='category_management'),    
    path('delete_category/<int:cate_id>', views.delete_category, name='delete_category'),
    path('update_category/<int:cate_id>/', views.update_category, name='update_category'),
    path('add_category', views.add_category, name='add_category'),

        
]
