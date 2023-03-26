from django.db import models

# Create your models here.
class Banner(models.Model):
    banner_name = models.CharField(max_length=100)
    # banner_image = models.ImageField(upload_to="banner_image")
    banner_image = models.TextField()
    note = models.CharField(max_length=100)
    discount = models.IntegerField()


    def __str__(self):
        return self.banner_name
    
    def get_images(self):
        # Return a list of image URLs from the images field
        return self.images.split(',')
    
class Carousel(models.Model):
    name = models.ForeignKey(Banner,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner_image')
    
    def __str__(self):
        return f'{self.name.banner_name}'
