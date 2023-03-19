from django.contrib import admin
from .models import *
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = [ 'cart_id']

class CartitemAdmin(admin.ModelAdmin):
    list_display = [ 'product', 'cart_id', 'quantity']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupan_code','is_expired','discount_price','minimum_amount']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','address','payment_mode','status','created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','price','quantity']



admin.site.register(Cart,CartAdmin)
admin.site.register(Cartitem,CartitemAdmin)
