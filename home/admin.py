from django.contrib import admin
from .models import *




@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['banner_name','note']


admin.site.register(Carousel)
admin.site.register(Admin_profile)

 
