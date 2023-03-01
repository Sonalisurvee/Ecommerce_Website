from django.db import models
from django.core.validators import MinValueValidator
from category.models import Category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    image = models.ImageField(upload_to='product_images',default='404.png')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    

class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    productimage = models.ImageField(upload_to='product_images',default='404.png')


    # def __str__(self):
    #     return self.product