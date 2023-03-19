from django.db import models
from store.models import Product
from account.models import Account,Address

# Create your models here.

class Coupon(models.Model):
    coupan_code = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=True)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

    def __unicode__(self):
        return self.coupan_code

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
   
    def __unicode__(self):
        return self.product

class Order(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)    
    total_price = models.FloatField(null=False)
    PAYMENT_CHOICES = (
        ('cod', 'Cash on Delivery'),
    )
    payment_mode = models.CharField(max_length=150, choices=PAYMENT_CHOICES, default='cod')
    payment_id = models.CharField(max_length=250,null=True)
    orderstatuses = (
        ('Pending','Pending'),
        ('Out for Shipping','Out for Shipping'),
        ('Completed','Completed'),
    )
    status = models.CharField(max_length=150,choices=orderstatuses,default='Pending') 
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.address)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __unicode__(self):
        return self.id
