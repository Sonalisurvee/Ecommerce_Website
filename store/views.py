from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Product,Product_Image,ReviewRating
from category.models import Category
from cart.models import CartItems,Cartt
# from cart.views import _cart_id
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from decimal import Decimal
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
import re
from django.core.exceptions import ValidationError

# -----------------------------------Product Management-Delete,edit and add --------------------------------


def product_management(request):
    categories = Category.objects.all()    
    products = Product.objects.all()
    return render(request, 'product/product_management.html', {'products': products,'categories': categories})


def delete_product(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    del_record = Product.objects.filter(id=product_id)
    del_record.delete()
    messages.success(request, f"{product.product_name} has been deleted from the list")    
    return redirect(product_management)   

 
def update_product(request, product_id):
    products = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            update_prod = Product.objects.get(id=product_id)
            product_image = request.FILES.get('image')
            if product_image:
                update_prod.image = product_image
                update_prod.save()
        except:
            pass
        product = request.POST.get('product')
        category = request.POST.get('category')
        product_description = request.POST.get('description')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        cat_instance = Category.objects.get(id=category)

        if not product:
            messages.warning(request, 'Product name shouldnt be empty')
            return redirect(product_management)
        
        if not all(char.isalpha() or char.isspace() for char in product) or len(product.strip()) == 0:
            messages.warning(request, 'Invalid entry for product name')
            return redirect(product_management)
        
        if not product_description:
            messages.warning(request, 'Product description shouldnt be empty')
            return redirect(product_management)
        
        if not all(char.isalpha() or char.isspace() or char in ["'", '.'] for char in product_description) or len(product_description.strip()) == 0:
            messages.warning(request, 'Invalid entry for product name')
            return redirect(product_management)   
        
        if not stock.isdigit():
            messages.warning(request,'Invalid entry for stock')
            return redirect(product_management)

        if not str(price).isnumeric() and 'e' not in price.lower():
            try:
                float(price)
                if float(price) < 0:
                    messages.warning(request, 'Price cannot be negative')
                    return redirect(product_management)
            except ValueError:
                messages.warning(request, 'Invalid entry for price')
                return redirect(product_management)

        if 'e' in price.lower() or float(price) > 1000000:
            messages.warning(request,'Enter only numbers, scientific notation not allowed, and the price should not exceed 1000000')
            return redirect(product_management)

        if Product.objects.filter(product_name=product).exclude(id=product_id).exists():
            messages.warning(request, 'A product with this name already exists.')
            return redirect(product_management)


        update_prod = Product.objects.filter(id=product_id)
        update_prod.update(
            product_name=product,
            category=cat_instance,
            product_description=product_description,
            stock=stock,
            price=price
        )

        context = {'product': products, 'categories': categories}
        messages.success(request, f"{products.product_name} has been updated")
        return redirect(product_management)
    else:
        messages.info(request, 'some field is empty')
        return render(request, 'product/product_management.html', context)

                                

def add_product(request):
    if request.method == 'POST':
        productname=request.POST['title']
        description=request.POST['description']
        category=request.POST['category']#here only the id of categorywill be stored
        stock=request.POST['stock']
        price=request.POST['price']

        if not productname:
            messages.warning(request, 'Product name shouldnt be empty')
            return redirect(product_management)
        
        if not all(char.isalpha() or char.isspace() for char in productname) or len(productname.strip()) == 0:
            messages.warning(request, 'Invalid entry for product name')
            return redirect(product_management)
        
        if Product.objects.filter(product_name=productname).exists():
            messages.info(request,"This product already exists")
            return redirect(product_management)

        try:
            product_image=request.FILES['image']
        except:
            messages.warning(request,'Thumbnail image is required for creating a product.')
            return redirect(product_management)
        
        if not description:
            messages.warning(request, 'Product description shouldnt be empty')
            return redirect(product_management) 

        if not all(char.isalpha() or char.isspace() or char in ["'", '.'] for char in description) or len(description.strip()) == 0:
            messages.warning(request, 'Invalid entry for product description')
            return redirect(product_management)  
        
        if not stock.isdigit():
            messages.warning(request,'Invalid entry for stock')
            return redirect(product_management)
                
        if not str(price).isnumeric() and 'e' not in price.lower():
            try:
                float(price)
                if float(price) < 0:
                    messages.warning(request, 'Price cannot be negative')
                    return redirect(product_management)
            except ValueError:
                messages.warning(request, 'Invalid entry for price')
                return redirect(product_management)

        if 'e' in price.lower() or float(price) > 1000000:
            messages.warning(request,'Enter only numbers, scientific notation not allowed, and the price should not exceed 1000000')
            return redirect(product_management)
    
        cat_instance = Category.objects.get(id=category)#for admin to view our category ,as cate is the forign key in product for we have to assig suprate instance for it so 
        # because we dint gave any related name to the category and now the id stored in the category will be stored in the category instance
        # 

        prod = Product.objects.create(
            product_name=productname,
            image=product_image,
            category=cat_instance,
            stock=stock,price=price,
            # slug=slug,
            product_description=description
            )
        
        try:
            product_image = request.FILES['image']
        except KeyError:
            product_image = None

        prod = Product.objects.create(
            product_name=productname,
            image=product_image,
            category=cat_instance,
            stock=stock,
            price=price,
            product_description=description
        )
        
        # this for loop i gave after multi_iamge then i got error saying 
        # The error message indicates that you are trying to assign a string value to the product field of the Product_Image model, but it expects an instance of the Product model.
        # To fix this,first create an instance of the 'Product' model, and then use that instance (prod) to create the Product_Image instances.
        # basically we stored the other data and now we are able to assign a name in product colum of 'Product_image' model
        # before the error was like cant assign name to product as there was no product exist or we dint add

        try:
            multi_imaeg = request.FILES.getlist('imagess')

            
            for image in multi_imaeg:
                Product_Image.objects.create(
                    product=prod, 
                    productimage=image
                    )      
            return redirect(product_management)
        except:
            pass

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
    try:
        if category_slug != None:#wat if slug is there
            categories=get_object_or_404(Category, slug=category_slug)
            products=Product.objects.filter(category=categories, is_available=True)
            product_count=products.count()
        else:
            products = Product.objects.all().filter(is_available=True)    
            product_count=products.count()  

        return render(request,'product/product_list.html',{'products': products,'product_count': product_count})
    except:
        return render(request,'404.html')
 

# -----------------------------------Product-Details --------------------------------



# Basically this is the view fun for viewing the details of single product 

def product_details(request, category_slug,product_slug):
    context = {}
    try:
        # size=request.Get.get('size')

        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        #this will show the single product based on the cate slug and prod slug 
        reviews = ReviewRating.objects.filter(product=single_product)

        cat=Product.objects.get(slug=product_slug)
        # this will only shows the cate matching product

        # user = request.user
        # cart= Cartt.objects.get_or_create(user = user,is_paid = False)        
        # in_cart = CartItems.objects.filter(carts=cart, products=single_product).exists()
        
       
        try:
            if request.GET.get('size'):
                size = request.GET.get('size')
                price = single_product.get_product_price_by_size(size)
                context['selected_size'] = size
                context['updates_price'] = price
                # updates_price = price
                # name 'updates_price' is not defined,this error i got wen i gave update_p outside the context.and i got this because 
        except:
            pass


    # if somebody enters wrong slug of product or try to search for anything n urls then it will raie an exception 
    # instead of raise e we can give the link to our 404 error page or any other link .
    # except Exception as e:
        # raise e    
    except Exception as e:
        return render(request,'404.html')
        
        

        
    products = Product_Image.objects.filter(product=single_product)    
    
    context.update({
        'single_product': single_product,
        # 'in_cart': in_cart,
        'cat':cat,
        'products':products,
        'reviews':reviews
    })
    print(context)

    return render(request,'product/single_product.html',context)













@login_required
def submit_review(request, product_id):
    if request.method == 'POST':
        try:
            review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=review)  # Checks whether the review of the product by the user exists.
                                                              # If exists, it will detect that review needs to be updated.
                                                              # If instance not passed, it will save it as a new review
            form.save()
            messages.success(request, 'Thank you! Your review has been updated')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            
            if form.is_valid():
                data = ReviewRating()
                data.title = form.cleaned_data['title']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.user = request.user
                data.product_id = product_id
                data.save()
                messages.success(request, 'Thank you! Your review have been saved.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
    messages.error(request, 'Not success')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


