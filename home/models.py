from django.db import models

# Create your models here.
class Banner(models.Model):
    banner_name = models.CharField(max_length=100)
    banner_image = models.ImageField(upload_to="banner_image")
    note = models.CharField(max_length=100)
    discount = models.IntegerField()

    def __str__(self):
        return self.banner_name