from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Category
from store.models import Product    
      
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
    products=get_object_or_404(Category,pk=cate_id)
    if request.method == 'POST':
        category=request.POST['category']
        description=request.POST['description']
        slug=request.POST['slug']  
        try:
            update_category = Category.objects.get(id=cate_id)
            #this update_c was given to get the perticular id wala img so that we can save it
            image=request.FILES['image']
            update_category.cat_image=image
            update_category.save()
        except:
            pass

        if Category.objects.filter(cat_name=category).exists():
            messages.info(request,"This category already exists")
            return redirect(category_management)
        else:
            update_category = Category.objects.filter(id=cate_id)  
        # this update_c was given to filter all the id in the category        
            update_category.update(cat_name=category,description=description,slug=slug)
            return redirect(category_management)

        #here both the update_c were imp because both play 2 diff roles 
    else:
        messages.info(request,'some field is empty')
        return render(request,'category/category_management.html')


def add_category(request):
    if request.method == 'POST':
        category = request.POST['category']
        description = request.POST['description']
        image=request.FILES['image']
        slug=request.POST['slug']  
        if Category.objects.filter(cat_name=category).exists():
            messages.info(request,"This category already exists")
            return redirect(category_management)
        else:
            cate = Category.objects.create(cat_name=category,description=description,cat_image=image,slug=slug)
            cate.save()           
        return redirect(category_management)   
  
    else:
        messages.info(request,'some field is empty')
        return redirect(add_category)
    

           
def simply(request):
        return render(request,'category/simply.html')