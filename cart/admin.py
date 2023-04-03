from django.contrib import admin
from .models import *
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = [ 'user']

class CartitemAdmin(admin.ModelAdmin):
    list_display = [ 'carts', 'products', 'variant']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['coupan_code','is_expired','discount_price','minimum_amount']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','grand_total','payment_method','is_paid','paid_date']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','delivery_address','payment','ordered_date']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','product','variant','order_status','quantity','item_total']

admin.site.register(Cartt,CartAdmin)
admin.site.register(CartItems,CartitemAdmin)

