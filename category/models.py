from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    cat_name=models.CharField(null=False,blank=False,unique=True,max_length=200)
    description=models.TextField()
    slug=models.SlugField(unique=True,null=True,blank=True)
    cat_image=models.ImageField(upload_to="category")
    status = models.BooleanField(default=False,help_text="0=default, 1=hidden")

    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.cat_name)
        super(Category ,self).save(*args , **kwargs)

    def get_url(self):
        return reverse('product_by_cate',args=[self.slug])

    def __str__(self):
        return self.cat_name
    

