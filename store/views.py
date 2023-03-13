from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Product
from category.models import Category
from cart.models import Cart,Cartitem
from cart.views import _cart_id
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q


# -----------------------------------Product-Delete,edit and add --------------------------------


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
        try:
            update_prod=Product.objects.get(id=product_id)
            product_image=request.FILES['image']
            update_prod.image=product_image
            update_prod.save()
        except:
            pass
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
    

# -----------------------------------Search --------------------------------


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:#if keyword checks whethe there is something in to search
            products = Product.objects.order_by('-created_at').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count=products.count()

    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request,'product/product_list.html',context)


# -----------------------------------Product-listing --------------------------------



def product_list(request,category_slug=None):
    categories=None
    products=None        
    if category_slug != None:#wat if slug is there
        categories=get_object_or_404(Category, slug=category_slug)
        products=Product.objects.filter(category=categories, is_available=True)
        product_count=products.count()
    else:
        products = Product.objects.all().filter(is_available=True)    
        product_count=products.count()    
    return render(request,'product/product_list.html',{'products': products,'product_count': product_count})


# -----------------------------------Product-Details --------------------------------


def product_details(request, category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        cat=Product.objects.get(slug=product_slug)

        if request.user.is_authenticated:
            in_cart = Cartitem.objects.filter(user=request.user,product=single_product).exists()
        else:
            in_cart = Cartitem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        # here cart__cart_id is ,cart is the colum in Cartitem whisch is the foreign key an dwant cart_id from CArt table so we gave double underscore  __ 
       
    except Exception as e:
        raise e    
    context={
        'single_product': single_product,
        'in_cart': in_cart,
        'cat':cat,
    }
    return render(request,'product/single_product.html',context)



def single_product(request):    
    return render(request,'product/single_product.html')



