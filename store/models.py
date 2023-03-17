from django.db import models
from django.core.validators import MinValueValidator
from category.models import Category
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product ,self).save(*args , **kwargs)


    def __str__(self):
        return self.product_name
    
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
