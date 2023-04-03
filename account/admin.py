from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name','username','last_login','is_active',)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('full_name','phone','state','house_name','default')


admin.site.register(Account, AccountAdmin)
admin.site.register(Address, AddressAdmin)
