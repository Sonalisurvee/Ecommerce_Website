from django.contrib import admin
from .models import *
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = [ 'cart_id']

class CartitemAdmin(admin.ModelAdmin):
    list_display = [ 'product', 'cart_id', 'quantity']

admin.site.register(Cart,CartAdmin)
admin.site.register(Cartitem,CartitemAdmin)
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(OrderItem)
