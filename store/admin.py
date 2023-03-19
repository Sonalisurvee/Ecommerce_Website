from django.contrib import admin
from .models import *


class ProductImageAdmin(admin.StackedInline):
    model = Product_Image

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','updated_at','is_available')
    inlines = [ProductImageAdmin]
    # prepopulated_fields = {'slug': ('product_name',)}
    

# this below deco will add new behaviour as well as register it
@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name','price']
    model = ColorVariant

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name','price']
    model = SizeVariant
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Product_Image)