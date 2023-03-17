from django.contrib import admin
from .models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug':('cat_name',)}
    # this was given for automatic generation of the slug with cat_name will be entered
    # but here it wil get generated only in django admin page not in admin panel
    # to get automaticly generated i gave a fun in cateeogry.models a save() fun
    list_display=('cat_name','slug')

admin.site.register(Category,CategoryAdmin)