from django.contrib import admin
from .models import *

# Register your models here.
class ProductImageAdmin(admin.StackedInline):
    model = Product_Image

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','updated_at','is_available')
    inlines = [ProductImageAdmin]
    # prepopulated_fields = {'slug': ('product_name',)}
    

    
admin.site.register(Product, ProductAdmin)
admin.site.register(Product_Image)