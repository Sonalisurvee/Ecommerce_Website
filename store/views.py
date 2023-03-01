from django.shortcuts import render,redirect,get_object_or_404
from .models import Product
from category.models import Category
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# Create your views here.

def product_management(request):
    categories = Category.objects.all()    
    products = Product.objects.all()
    return render(request, 'product/product_management.html', {'products': products,'categories': categories})

def delete_product(request,product_id):
    del_record = Product.objects.filter(id=product_id)
    del_record.delete()
    return redirect(product_management)   


def update_product(request,product_id):
    products=get_object_or_404(Product,pk=product_id)
    categories = Category.objects.all()    
    if request.method == 'POST':
        update_prod=Product.objects.get(id=product_id)
        product_image=request.FILES['image']
        update_prod.image=product_image
        update_prod.save()

        product=request.POST['product']
        category=request.POST['category']
        product_description=request.POST['description']
        stock=request.POST['stock']
        price=request.POST['price']
        cat_instance = Category.objects.get(id=category)
         
        update_prod=Product.objects.filter(id=product_id)
        update_prod.update(product_name=product,category=cat_instance,product_description=product_description,stock=stock,price=price)
        context = {'product': products, 'categories': categories}
        return redirect(product_management)

    else:    
        messages.info(request,'some field is empty')
        return render(request,'product/product_management.html', context)



def add_product(request):
    if request.method == 'POST':
        productname=request.POST['title']
        slug=request.POST['slug']
        product_image=request.FILES['image']
        description=request.POST['description']
        category=request.POST['category']#here only the id of categorywill be stored
        stock=request.POST['stock']
        price=request.POST['price']
        cat_instance = Category.objects.get(id=category)#for admin to view our category ,as cate is the forign key in product for we have to assig suprate instance for it so 
        # because we dint gave any related name to the category and now the id stored in the category will be stored in the category instance
        # 
        prod = Product.objects.create(product_name=productname,image=product_image,category=cat_instance,stock=stock,price=price,slug=slug,product_description=description)
        prod.save()           
        return redirect(product_management)
  
    else:
        return redirect(add_product)


def product_list(request):
    dict_products = {
        'products': Product.objects.all().order_by('id')
    }
    return render(request,'product/product_list.html',dict_products)
