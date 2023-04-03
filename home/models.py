from django.db import models
from account.models import Account,Address

# Create your models here.
class Banner(models.Model):
    banner_name = models.CharField(max_length=100)
    banner_image = models.ImageField(upload_to="banner_image")
    # banner_image = models.TextField()
    note = models.CharField(max_length=100)
    discount = models.IntegerField()


    def __str__(self):
        return self.banner_name
    
    # def get_images(self):
    #     # Return a list of image URLs from the images field
    #     return self.images.split(',')
    
class Carousel(models.Model):
    carousel_name = models.ForeignKey(Banner,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner_image')
    
    def __str__(self):
        return f'{self.carousel_name.banner_name}'


class Admin_profile(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    about = models.CharField(max_length=300)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile')

    def __str__(self):
        return f'{self.user.username}'
