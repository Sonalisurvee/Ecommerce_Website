from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect,HttpResponse
from django.contrib import messages
from .models import Banner,Carousel,Admin_profile
from account.models import Account,Address
from category.models import Category
from cart.models import Coupon,Order,OrderItem
from store.models import Product,ReviewRating,Varitaion,SizeVariant
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import razorpay
from django.conf import settings
from django.core.mail import send_mail




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


# -----------------------------------------user_management-----------------------------------------

@login_required(login_url='/login')
def user_management(request):
    dict_user={
        'users':Account.objects.filter(is_staff=False).order_by('id')
    }    
    return render(request,'adminpanel/user_management.html',dict_user)

@login_required(login_url='/login')
def block_unblock(request,user_id):
    user=get_object_or_404(Account,id=user_id) #is user that we are checking exits then it will store it in the user variable else it will throw man 404 error
    if user.is_active:
        user.is_active=False#just converting the active status of the user to inaction
        user.save()
        messages.success(request,f"{user.username} has been blocked")
        return redirect(user_management)
    else:
        user.is_active=True
        user.save()
        messages.success(request,f"{user.username} has been Unblocked")
        return redirect(user_management)


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
    

def delet_image(request,carousel_id):
    delet_banner_image = Carousel.objects.filter(id=carousel_id) 
    delet_banner_image.delete()
    return redirect(banner_management)    


# def delet_image(request, carousel_id):
#     delet_banner_image = Carousel.objects.get(id=carousel_id) # Get the carousel object to be deleted
#     image_path = os.path.join(settings.MEDIA_ROOT, str(delet_banner_image.image)) # Get the path to the image file
#     os.remove(image_path) # Delete the image file from the server's file system
#     delet_banner_image.delete() # Delete the record from the database
#     return redirect(banner_management)



# -----------------------------------------404-----------------------------------------


def error_404(request,exception):
    return render(request,'404.html')


# -----------------------------------------Order management-----------------------------------------

@login_required(login_url='/login')
def order_management(request):
    context = {
        'orders':Order.objects.all().order_by('-id')
    }
    return render(request,'adminpanel/order_management.html',context)


def view_order(request,id):
    try:
        order = Order.objects.get(id=id)
        order_items = OrderItem.objects.filter(order=order)
    except:
        pass 

    dict_order = {
        'order_items':order_items,
        'statuses' : OrderItem.STATUS
    }    
    return render(request, 'adminpanel/view_order.html',dict_order)


def update_status(request, id):
    if request.method == 'POST':
        try:
            order = OrderItem.objects.get(id=id)
            status = request.POST['order_status']
            order.order_status = status
            order.save()
            messages.success(request, 'Status updated succesfully')
            # email 
            mess=f'Hello\t{order.user.first_name},\n Your order {order.product.product_name} with Order ID: {order.order.order_id} has been {order.order_status} successfully\n Track your order status in our website \n Thank you' 
            send_mail(
                    'Order status',
                    mess,
                    settings.EMAIL_HOST_USER,
                    [order.user.email],
                    fail_silently=False
                )
            # email stop
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        except OrderItem.DoesNotExist:
            messages.error(request, 'Something gone wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            



# -----------------------------------------Coupan management-----------------------------------------

@login_required(login_url='/login')
def coupan_management(request):
    dict_coupon = {
        'coupon':Coupon.objects.all().order_by('id')
    }
    return render(request,'adminpanel/coupan_management.html',dict_coupon)


def delete_coupon(request,coupan_id):
    coupon=get_object_or_404(Coupon,pk=coupan_id)
    del_record = Coupon.objects.filter(id=coupan_id)
    del_record.delete()
    messages.warning(request,f"Deleted the {coupon.coupan_code} coupon")
    return redirect(coupan_management)


def update_coupon(request,coupan_id):
    coupon=get_object_or_404(Coupon,pk=coupan_id)
    if request.method == 'POST':
        coupan=request.POST['coupan']
        discount=request.POST['discount']
        minimum=request.POST['minimum']  

        if not coupan:
            messages.info(request, 'Coupon field is empty')
            return redirect(coupan_management)  
        
        if not all(char.isalpha() or char.isspace() for char in coupan) or len(coupan.strip()) == 0:
            messages.warning(request, 'Invalid entry for coupan name')
            return redirect(coupan_management)
     
        if Coupon.objects.filter(coupan_code=coupon).exclude(id=coupan_id).exists():
            messages.info(request,"This coupon already exists")
            return redirect(coupan_management)   
         
        if float(discount) > 1000000:
            messages.warning(request,'Enter only numbers, scientific notation not allowed as discount price')
            return redirect(coupan_management) 
          
        if not discount.isdigit():
            messages.warning(request,'Enter only numbers as discount price and no negetive number')
            return redirect(coupan_management)
                
        if not minimum.isdigit():
            messages.warning(request,'Enter only numbers as minimum amount and no negetive number')
            return redirect(coupan_management)
        
        if float(minimum) > 1000000:
            messages.warning(request,'Enter only numbers, scientific notation not allowed as minimum amount')
            return redirect(coupan_management)
            
        else:
            update_coupon = Coupon.objects.filter(id=coupan_id)  
            update_coupon.update(coupan_code=coupan,discount_price=discount,minimum_amount=minimum)
            messages.success(request,f"Updated the {coupon.coupan_code} coupon")
            return redirect(coupan_management)       

    else:
        messages.info(request,'some field is empty')
        return render(request,'adminpanel/coupan_management.html')
    

def add_coupon(request):
    if request.method == 'POST':
        coupon = request.POST['coupon']
        discount = request.POST['discount']
        minimum=request.POST['minimum']  

        if not coupon:
            messages.info(request, 'Coupon field is empty')
            return redirect(coupan_management)  
        
        if not all(char.isalpha() or char.isspace() for char in coupon) or len(coupon.strip()) == 0:
            messages.warning(request, 'Invalid entry for coupan name')
            return redirect(coupan_management)   
        
        if float(discount) > 1000000:
            messages.warning(request,'Enter only numbers, scientific notation not allowed as discount price')
            return redirect(coupan_management)    

        if not discount.isdigit():
            messages.warning(request,'Enter only numbers as discount price')
            return redirect(coupan_management) 
        
        if float(minimum) > 1000000:
            messages.warning(request,'Enter only numbers, scientific notation not allowed as minimum amount')
            return redirect(coupan_management)   
         
        if not minimum.isdigit():
            messages.warning(request,'Enter only numbers as minimum amount')
            return redirect(coupan_management)
        
        if Coupon.objects.filter(coupan_code=coupon).exists():
            messages.info(request,"This coupon already exists")
            return redirect(coupan_management)
        else:
            coupan = Coupon.objects.create(coupan_code=coupon,discount_price=discount,minimum_amount=minimum)
            coupan.save()      
            messages.success(request,f"New coupon '{coupan.coupan_code}' has been created")
        return redirect(coupan_management)   
  
    else:
        messages.info(request,'some field is empty')
        return redirect(add_coupon)
    

def expired(request,coupan_id):
    c=get_object_or_404(Coupon,id=coupan_id) #is user that we are checking exits then it will store it in the user variable else it will throw man 404 error
    if c.is_expired:
        c.is_expired=False#just converting the active status of the user to inaction
        c.save()
        return redirect(coupan_management)
    else:
        c.is_expired=True
        c.save()
        return redirect(coupan_management)                                                   
    


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
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET_KEY))
    order = Order.objects.get(user=request.user, order_id=order_id)
    payment_id = order.payment.transaction_id
    item = OrderItem.objects.get(order=order, id=item_id)
    item_amount = int(item.item_total * 100)

    refund = client.payment.refund(payment_id,{'amount':item_amount})

    if refund is not None:
        item.order_status = 'Refunded'
        item.variantion.stock += item.quantity
        item.save()

        return render(request, 'cart/refund_success.html',{'order_id':order_id})
    
    else:
        return HttpResponse('Payment Not Captured')


# -----------------------------------------Order management admin side-----------------------------------------


@login_required(login_url='/login')
def sales(request):
    context = {}

    if request.method == 'POST':

        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')

        if start_date == '' or end_date == '':
            messages.error(request,'Give date first')
            return redirect(sales)

        order_items = OrderItem.objects.filter(order__ordered_date__gte=start_date, order__ordered_date__lte=end_date)
        if order_items:
            print(order_items)
            context.update(sales = order_items,s_date=start_date,e_date = end_date)
        else:
            messages.error(request,'no data found')
    return render(request,'adminpanel/sales_report.html',context)

@login_required(login_url='/login')
def admin_profile(request):
        admin = Admin_profile.objects.get(user = request.user)


        # profile = Account
        return render(request,'adminpanel/admin_profile.html',{'admin': admin})

@login_required(login_url='/login')
def admin_profile_update(request,admin_id):
    
        return render(request,'adminpanel/admin_profile.html')
    
    


# -----------------------------------------------review managment-----------------------------------------------

@login_required(login_url='/login')
def review_management(request):
    dict_review = {
        'review': ReviewRating.objects.all().order_by('id')        
    }

    return render(request,'adminpanel/admin_review.html',dict_review)

def delete_review(request,id):
    review = get_object_or_404(ReviewRating,pk=id)
    delete_reviews = ReviewRating.objects.filter(id=id)
    delete_reviews.delete()
    messages.warning(request,f"Deleted the {review.title} review")
    return redirect(review_management)

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
    



def about(request):
    return render(request,'userpanel/about.html')