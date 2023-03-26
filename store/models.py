from django.db import models
from django.core.validators import MinValueValidator
from category.models import Category
from django.urls import reverse
from django.utils.text import slugify
from account.models import Account


class ColorVariant(models.Model):
   color_name = models.CharField(max_length=100)
   price = models.IntegerField(default=0)

   def __str__(self):
        return self.color_name

class SizeVariant(models.Model):
   size_name = models.CharField(max_length=100)
   price = models.IntegerField(default=0)

   def __str__(self):
        return self.size_name

class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug=models.SlugField(unique=True,null=True,blank=True)
    image = models.ImageField(upload_to='product_images',default='404.png')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    color_variant = models.ManyToManyField(ColorVariant,blank=True)
    size_variant = models.ManyToManyField(SizeVariant,blank=True)



    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product ,self).save(*args , **kwargs)


    def __str__(self):
        return self.product_name

# this funtion is used to add the price according to the size
    def get_product_price_by_size(self ,size):
        return self.price + SizeVariant.objects.get(size_name = size).price
    
    # self.price is the exsiting price nd we r adding this price with the new sizevar
    # price,we gave .price in the end because 


    def get_url(self):
        return reverse('product_details',args=[self.category.slug,self.slug])    
    
    #here self inside args is our Product model
    # here category means category column
    # here slug means the category slug presnt in the Category model

    # here next self means Product model
    #  slug menas te slug present n the Product model


class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    productimage = models.ImageField(upload_to='product_images',default='404.png')

    def __str__(self):
        return f'{self.product.product_name}'



class Varitaion(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    size_variant = models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,null=True,blank=True)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.size_variant.size_name
    


class ReviewRating(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    review = models.TextField(blank=True, null=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

