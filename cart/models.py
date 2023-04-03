from django.db import models
from store.models import Product,SizeVariant,Varitaion
from account.models import Account,Address
from decimal  import Decimal


class Coupon(models.Model):
    coupan_code = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=True)
    discount_price = models.PositiveIntegerField(default=100)
    minimum_amount = models.PositiveIntegerField(default=500)

    def __unicode__(self):
        return self.coupan_code

    
class Cartt(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True,blank=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='carts',null=True)
    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=100 ,null=True, blank=True,unique=True)
    cart_id = models.CharField(max_length=250,blank=True)

    def __unicode__(self):
        return self.user
 
    def get_cart_total(self):
        cart_items = CartItems.objects.filter(carts=self.id)
        price = []
        for cart_item in cart_items:
            product_price = cart_item.products.price
            quantity = cart_item.quantity
            total_price = product_price * quantity
            price.append(total_price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant.price
                total_size_price = size_variant_price * quantity
                price.append(total_size_price)
        print(price)
        return sum(price)
    
    # Tax of cart_total
    def get_tax(self):
        return round(self.get_cart_total() * Decimal(2.5/100),2)
    
    # tax + cart_total
    def get_grand_total(self):
        cart_total = self.get_cart_total()
        tax = self.get_tax()
        grand_total = cart_total + tax
        if self.coupon:
            grand_total -= self.coupon.discount_price
        return grand_total
    
  

class CartItems(models.Model):
    carts = models.ForeignKey(Cartt, on_delete=models.CASCADE,related_name='cart_items')
    products = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True)
    size_variant = models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    variant = models.ForeignKey(Varitaion, on_delete=models.SET_NULL, null=True, blank=True)

    
    def __unicode__(self):
        return self.carts

    def get_product_price(self):
        price = [self.products.price]

        if self.size_variant:
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
        return sum(price)   
 
    
    def sub_total(self):
        price = [self.products.price]
        if self.size_variant:
            price.append(self.size_variant.price)
        sub_total = sum(price) * self.quantity
        return sub_total
    
   
# for invioce and for order payment hign we neeeded this
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    cart_total = models.PositiveIntegerField()
    tax = models.PositiveIntegerField()
    grand_total = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=30, default='RazorPay')
    is_paid = models.BooleanField(default=True)
    paid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.transaction_id
    

class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.id} of {self.user}'
    
    

class OrderItem(models.Model):
    STATUS = (
        ('Ordered', 'Ordered'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded')
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.CharField(max_length=100, null=True,blank=True)
    variantion = models.ForeignKey(Varitaion,on_delete=models.CASCADE,null=True,blank=True)
    order_status = models.CharField(max_length=20, choices=STATUS, default='Ordered')
    item_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    item_total = models.PositiveIntegerField()

    def __unicode__(self):
        return self.quantity

    def quantity_added(self):
        total = self.item_price * self.quantity
        return total
    
    def calculate_order_total(self):
        order_items = OrderItem.objects.filter(order=self.order)
        print()
        order_total = []
        total_price = 0
        for order_item in order_items:           
            total_price = total_price + order_item.item_total
            order_total.append(total_price)

        return sum(order_total)