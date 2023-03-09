from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Account,Address

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name','username','last_joined','is_active',)

admin.site.register(Account)
admin.site.register(Address)
