from django.contrib import admin
from .models import *

class BannerImageAdmin(admin.StackedInline):
    model = Carousel


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['banner_name','note']
    inlines = [BannerImageAdmin]


@admin.register(Carousel)
class CarousalAdmin(admin.ModelAdmin):
    list_display = ['name']
