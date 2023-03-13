from django.db import models
from store.models import Product
from account.models import Account

# Create your models here.

class Coupon(models.Model):
    coupan_code = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=True)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)



class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.cart_id
    
    
class Cartitem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True,blank=True)

    def sub_total(self):
        return self.product.price * self.quantity
   
    # def grand_total(self):
    #     if self.coupon:
    #         return self.product.price * self.quantity - coupon.discount_price
        


    def grand_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_itemm in cart_items:
            price += (cart_itemm.product.price * cart_itemm.quantity)
        if self.coupon:
            return price - self.coupon.discount_price
        # return total or 0  # return 0 if total is None or False


    # def get_cart_total(self):
    #     if self.coupon:
    #         return sum()
            
   

    def __unicode__(self):
        return self.product
    





