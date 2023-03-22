from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Product,Product_Image
from category.models import Category
from cart.models import CartItems,Cartt
# from cart.views import _cart_id
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q


# -----------------------------------Product Management-Delete,edit and add --------------------------------


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
        update_prod.update(
            product_name=product,
            category=cat_instance,
            product_description=product_description,
            stock=stock,price=price
            )
        context = {
            'product': products, 
            'categories': categories,
            }
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

        multi_imaeg = request.FILES.getlist('imagess')


        cat_instance = Category.objects.get(id=category)#for admin to view our category ,as cate is the forign key in product for we have to assig suprate instance for it so 
        # because we dint gave any related name to the category and now the id stored in the category will be stored in the category instance
        # 
        prod = Product.objects.create(
            product_name=productname,
            image=product_image,
            category=cat_instance,
            stock=stock,price=price,
            slug=slug,
            product_description=description
            )
        
        # this for loop i gave after multi_iamge then i got error saying 
        # The error message indicates that you are trying to assign a string value to the product field of the Product_Image model, but it expects an instance of the Product model.
        # To fix this,first create an instance of the 'Product' model, and then use that instance (prod) to create the Product_Image instances.
        # basically we stored the other data and now we are able to assign a name in product colum of 'Product_image' model
        # before the error was like cant assign name to product as there was no product exist or we dint add


        
        for image in multi_imaeg:
            Product_Image.objects.create(
                product=prod, 
                productimage=image
                )      
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


# this is to view all the products and get perticuler cate product (by giving cate slug)
# category_slug=None gave because we r listng all products and perticular product ,so if cate_slug is empty then id wll list all product and ro avoid error
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



# Basically this is the view fun for viewing the details of single product 

def product_details(request, category_slug,product_slug):
    context = {}
    try:
        # size=request.Get.get('size')

        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        #this will show the single product based on the cate slug and prod slug 

        cat=Product.objects.get(slug=product_slug)
        # this will only shows the cate matching product

        # user = request.user
        # cart= Cartt.objects.get_or_create(user = user,is_paid = False)        
        # in_cart = CartItems.objects.filter(carts=cart, products=single_product).exists()
        
       

        if request.GET.get('size'):
            size = request.GET.get('size')
            price = single_product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updates_price'] = price
            # updates_price = price
            # name 'updates_price' is not defined,this error i got wen i gave update_p outside the context.and i got this because 



    # if somebody enters wrong slug of product or try to search for anything n urls then it will raie an exception 
    # instead of raise e we can give the link to our 404 error page or any other link .
    except Exception as e:
        raise e    
        
        

        
    products = Product_Image.objects.filter(product=single_product)    
    
    context.update({
        'single_product': single_product,
        # 'in_cart': in_cart,
        'cat':cat,
        'products':products,
    })
    print(context)

    return render(request,'product/single_product.html',context)