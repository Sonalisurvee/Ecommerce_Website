from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['user','product','wishlist','is_active']

admin.site.register(Wishlist)
