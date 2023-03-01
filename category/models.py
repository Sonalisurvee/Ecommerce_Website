from django.db import models

# Create your models here.
class Category(models.Model):
    cat_name=models.CharField(null=False,blank=False,unique=True,max_length=200)
    description=models.TextField()
    slug=models.SlugField(unique=True)
    cat_image=models.ImageField(upload_to="category")

    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'

    def __str__(self):
        return self.cat_name
    

