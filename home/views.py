from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from .models import Banner,Carousel
from account.models import Account,Address
from category.models import Category
from cart.models import Coupon,Order,OrderItem
from store.models import Product,Varitaion,SizeVariant
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import razorpay
from django.conf import settings
import os
from datetime import datetime, timedelta

def index(request):   
    banner = Banner.objects.all().order_by('id')
    banners = Carousel.objects.all().order_by('id')
    category = Category.objects.all().order_by('id')
    most_sold_product = Product.objects.all().order_by('id')[:3]

    dict_banner={
        'banners': banners,
        'banner': banner,
        'category': category,
        'product' : most_sold_product
    }    
    return render(request,'userpanel/index.html',dict_banner)


# -----------------------------------------user_profile-----------------------------------------


@login_required(login_url='/login')
def profile(request):
    context = {
        'user_addresses': Address.objects.filter(customer=request.user).order_by('id'),
        'order':Order.objects.filter(user = request.user)
    }
    return render(request, 'userpanel/profile.html',context)


@login_required(login_url='/login')
def update_profile(request,user_id):
    user=get_object_or_404(Account,pk=user_id)
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        number=request.POST['number']       
               
        update_user = Account.objects.filter(id=user_id)  
        update_user.update(first_name=fname,last_name=lname,phone_number=number)
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect(profile)     
    else:
        messages.info(request,'some field is empty')
        return render(request,'userpanel/profile.html',{'user':user})


# -----------------------------------------Banner_management-----------------------------------------
@login_required(login_url='/login')
def banner_management(request):
    dict_banner={
        'banners': Banner.objects.all().order_by('id'),
        'carousal': Carousel.objects.all().order_by('id')
    }    
    return render(request,'adminpanel/banner_management.html',dict_banner)


def banner_delete(request,banner_id):
    delet_banner = Banner.objects.filter(id=banner_id)   
    delet_banner.delete()
    messages.success(request, 'Deleted succesfully')
    return redirect(banner_management)

def banner_edit(request,banner_id):
    banner=get_object_or_404(Banner,pk=banner_id)
    if request.method=='POST':
        name=request.POST['name']
        description=request.POST['description']
        discount=request.POST['discount']        
        image=request.FILES.getlist('image') 
                
        if not name:
            messages.warning(request, 'Banner name shouldnt be empty')
            return redirect(banner_management)
        
        if not all(char.isalpha() or char.isspace() for char in name) or len(name.strip()) == 0:
            messages.warning(request, 'Invalid entry for banner name')
            return redirect(banner_management)
        
        if Coupon.objects.filter(coupan_code=name).exclude(id=banner_id).exists():
            messages.info(request,"This banner already exists")
            return redirect(banner_management)

        if not description:
            messages.warning(request, 'Banner description shouldnt be empty')
            return redirect(banner_management)

        if not all(char.isalpha() or char.isspace() or char in ["'", '.'] for char in description) or len(description.strip()) == 0:
            messages.warning(request, 'Invalid entry for banner decription')
            return redirect(banner_management)  

        if not discount.isdigit():
            messages.warning(request,'Enter only positive number')
            return redirect(banner_management)
        
        if int(discount) > 1000000:
            messages.warning(request,'Enter only number')
            return redirect(banner_management)
        

        update_banner=Banner.objects.get(id=banner_id)
        # update_banner=Banner.objects.filter(id=banner_id)
        # update_banner.update(banner_name=name,note=description,discount=discount)
        update_banner.banner_name=name
        update_banner.note=description
        update_banner.discount=discount
        update_banner.save()
    
        # for carousel in update_banner.carousel_set.all():
        #     image_path = carousel.image.path
        #     os.remove(image_path)
        #     carousel.delete()            

        for im in image:
            carousel = Carousel.objects.create(
                carousel_name = update_banner,
                image =im
                )
            carousel.save() 
        messages.info(request,f"{update_banner.banner_name} got updated")        
        return redirect(banner_management)
    else:
        messages.info(request,'some field is empty')
        return render(request,'adminpanel/banner_management.html',{'banner':banner})
    

# def delet_image(request,carousel_id):
#     delet_banner_image = Carousel.objects.filter(id=carousel_id) 
#     delet_banner_image.delete()
#     return redirect(banner_management)    

# this will delete the image from the servers file
def delet_image(request, carousel_id):
    delet_banner_image = Carousel.objects.get(id=carousel_id) # Get the carousel object to be deleted
    image_path = os.path.join(settings.MEDIA_ROOT, str(delet_banner_image.image)) # Get the path to the image file
    os.remove(image_path) # Delete the image file from the server's file system
    delet_banner_image.delete() # Delete the record from the database
    return redirect(banner_management)



# -----------------------------------------404-----------------------------------------


def error_404(request,exception):
    return render(request,'404.html')


# -----------------------------------------Order management user side-----------------------------------------


@login_required(login_url='/login')
def orders_list(request):

    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'cart/order_list.html', {'orders' : orders})

@login_required(login_url='/login')
def order_details(request,order_id):
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
    except:
        pass 
    return render(request, 'cart/order_details.html', {'order_items' : order_items})

@login_required(login_url='/login')
def order_tracking(request, item_id):
    current_date = timezone.now()
    item = OrderItem.objects.get(id=item_id)
    context = {
        'item' : item,
        'current_date' : current_date
    }
    return render(request, 'cart/order_tracking.html' ,context)

@login_required(login_url='/login')
def order_invoice(request, order_id):
    order = Order.objects.get(id=order_id,user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    context = {
        'order' : order,
        'order_items' : order_items
    }
    return render(request, 'cart/invoice.html',context)


@login_required(login_url='/login')
def cancel_order(request, item_id=None, order_id=None):        
    client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
    order = Order.objects.get(user=request.user, order_id=order_id)
    payment_id = order.payment.transaction_id
    item = OrderItem.objects.get(order=order, id=item_id)
    item_amount = int(item.item_total * 100)

    refund = client.payment.refund(payment_id,{'amount':item_amount})

    if refund is not None:
        item.order_status = 'Refunded'
        item.variantion.stock += item.quantity
        item.save()
        item.variantion.save()

        return render(request, 'cart/refund_success.html',{'order_id':order_id})
    
    else:
        return HttpResponse('Payment Not Captured')


# --------------------------------------------------Sales------------------------------------------------------


@login_required(login_url='/login')
def sales(request):
    context = {}

    if request.method == 'POST':

        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')

        if start_date == '' or end_date == '':
            messages.error(request,'Give date first')
            return redirect(sales)
        
        if start_date ==  end_date :
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = OrderItem.objects.filter(order__ordered_date__date=date_obj.date())
            if order_items:
                context.update(sales = order_items,s_date=start_date,e_date = end_date)
                return render(request,'adminpanel/sales_report.html',context)
            else:
                messages.error(request,'no data found')
                return redirect(sales)

        order_items = OrderItem.objects.filter(order__ordered_date__gte=start_date, order__ordered_date__lte=end_date)
        if order_items:
            print(order_items)
            context.update(sales = order_items,s_date=start_date,e_date = end_date)
        else:
            messages.error(request,'no data found')
    return render(request,'adminpanel/sales_report.html',context)


# -----------------------------------------------Varaint managment-----------------------------------------------

@login_required(login_url='/login')
def variant_management(request):
    dict_variant = {
        'variations' : Varitaion.objects.all().order_by('id'),
        'products' : Product.objects.all().order_by('id'),
        'size' : SizeVariant.objects.all().order_by('id')
    }
    return render(request,'adminpanel/variants.html',dict_variant)

def variant_delete(request,id):
    variant = get_object_or_404(Varitaion,pk=id)
    delete_variant = Varitaion.objects.get(id=id)
    delete_variant.delete()
    messages.warning(request,f"Deleted the {variant.size_variant} on {variant.product}")    
    return redirect(variant_management)

def variant_edit(request,id):
    variant = get_object_or_404(Varitaion,pk=id)
    if request.method == 'POST':
        product = request.POST['product']
        size = request.POST['size']
        stock = request.POST['stock']

        products = Product.objects.get(product_name = product)
        sizes = SizeVariant.objects.get(size_name = size)

        # these aboe both are the instance like product and size_name like product and size_variant are in the variation and both are the forgin fkey so to stoe it we need the posted value as the instance ,
        edit_variant = Varitaion.objects.filter(id=id)
        edit_variant.update(
            product=products,
            size_variant=sizes,
            stock=stock
            )
        messages.success(request,f"Updated the variant on {variant.product}")
        return redirect(variant_management)
    else:
        messages.info(request,'some field is empty')
        return redirect(variant_management)

def add_variant(request):
    if request.method == 'POST':
        product = request.POST['product']
        size = request.POST['size']
        stock = request.POST['stock']

        products = Product.objects.get(product_name = product)
        sizes = SizeVariant.objects.get(size_name = size)
        edit_variant = Varitaion.objects.create(
            product=products,
            size_variant=sizes,
            stock=stock
            )
        edit_variant.save()
        messages.success(request,"gfhj")
        return redirect(variant_management)
    else:
        messages.info(request,'some field is empty')
        return redirect(variant_management)
    

# ----------------------------------------------------------About page for user------------------------------------------------------

def about(request):
    return render(request,'userpanel/about.html')