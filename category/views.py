from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Category
from store.models import Product 
import re

      
# -----------------------------------Category-Delete,edit and add --------------------------------

    
def category_management(request):
    dict_cate={
        'cate': Category.objects.all().order_by('id')
    }
    return render(request,'category/category_management.html',dict_cate)
    

def delete_category(request,cate_id):
    del_record = Category.objects.filter(id=cate_id)
    del_record.delete()
    return redirect(category_management)


def update_category(request,cate_id):
    category1=Category.objects.get(id=cate_id)
    if request.method == 'POST':
        category=request.POST['category']
        description=request.POST['description']

        if Category.objects.filter(cat_name=category).exclude(id=cate_id).exists():
            messages.info(request,"This category already exists")
            return redirect(category_management)

        if not category:
            messages.info(request, 'Category field is empty')
            return redirect(category_management)  
        
        if not all(char.isalpha() or char.isspace() for char in category) or len(category.strip()) == 0:
            messages.warning(request, 'Invalid entry for category name')
            return redirect(category_management)
        
        if not all(char.isalpha() or char.isspace() or char in ["'", '.'] for char in description) or len(description.strip()) == 0:
            messages.warning(request, 'Invalid entry for category description')
            return redirect(category_management)  
         

        # here description was not getting updated because of if condinti given to the cat_name = category.exists, so we saved the description before onyly
        category1.description = description
        category1.save()
        # this i gave here for auto slug generation as slug is generated auto in because we gave save slug in the models
        category1.cat_name = category
        category1.save()
         
        try:
            update_category = Category.objects.get(id=cate_id)
            #this update_c was given to get the perticular id wala img so that we can save it
            image=request.FILES['image']
            update_category.cat_image=image
            update_category.save()
        except:
            pass        

        update_category = Category.objects.filter(id=cate_id)  
    # this update_c was given to filter all the id in the category        
        update_category.update(cat_name=category,description=description)
        messages.info(request,"Cate got updated")
        return redirect(category_management)

        #here both the update_c were imp because both play 2 diff roles 
    else:
        messages.info(request,'some field is empty')
        return render(request,'category/category_management.html')


def add_category(request):
    if request.method == 'POST':
        category = request.POST['category']
        description = request.POST['description']     
      
        if Category.objects.filter(cat_name=category).exists():
            messages.info(request,"This category already exists")
            return redirect(category_management)

        if not category:
            messages.info(request, 'Category field is empty')
            return redirect(category_management)  
        
        if not all(char.isalpha() or char.isspace() for char in category) or len(category.strip()) == 0:
            messages.warning(request, 'Invalid entry for category name')
            return redirect(category_management)
        
        try:
            image=request.FILES['image']
        except:
            messages.warning(request,'image is required for adding new category.')
            return redirect(category_management)        
        
        if not all(char.isalpha() or char.isspace() or char in ["'", '.'] for char in description) or len(description.strip()) == 0:
            messages.warning(request, 'Invalid entry for category description')
            return redirect(category_management)      
        
        cate = Category.objects.create(cat_name=category,description=description,cat_image=image)
        cate.save()  
        messages.info(request,"New category got created")         
        return redirect(category_management)   
  
    else:
        messages.info(request,'some field is empty')
        return redirect(add_category)
