from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect,HttpResponse
from django.contrib import messages
from .models import Banner,Carousel
from account.models import Account,Address
from category.models import Category
from cart.models import Coupon,Order,OrderItem,Payment
from store.models import Product
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import razorpay
from django.conf import settings
from django.db.models import  Sum
import os
import re



def index(request):   
    banner = Banner.objects.all().order_by('id')
    banners = Carousel.objects.all().order_by('id')
    category = Category.objects.all().order_by('id')

    dict_banner={
        'banners': banners,
        'banner': banner,
        'category': category,

    }    
    return render(request,'userpanel/index.html',dict_banner)


@login_required(login_url='/login')
def admin_index(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        user = Account.objects.all().count()
        product = Product.objects.all().count()
        category = Category.objects.all().count()
        sales = OrderItem.objects.count()
        orders = Order.objects.all().count()
        item = OrderItem.objects.all()
        delivered_orders = OrderItem.objects.filter().values('item_total')
        revenue = 0

        for order in delivered_orders:        
            revenue += order['item_total']

        recent_sale = OrderItem.objects.all().order_by('-id')[:5]
        total_income = Payment.objects.aggregate(Sum('grand_total'))['grand_total__sum']
        total_income = round(total_income, 2)


        context = {
            'user': user,
            'category': category,
            'product': product,
            'sales': sales,
            'orders': orders,
            'item': item,
            'total_income': total_income,        
            'recent_sales':recent_sale,
        }

        return render(request, 'adminpanel/admin_index.html',context)
    else:
        return redirect('/')
    


# -----------------------------------------user_management-----------------------------------------


def user_management(request):
    dict_user={
        'users':Account.objects.filter(is_staff=False).order_by('id')
    }    
    return render(request,'adminpanel/user_management.html',dict_user)


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



#---
def update_profile(request,user_id):
    user=get_object_or_404(Account,pk=user_id)
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        number=request.POST['number']       
        if not fname:
            messages.info(request,'First name is missing')
            return redirect(profile)
        if not lname:
            messages.info(request,'last name is missing')
            return redirect(profile)

        if not all(char.isalpha() or char.isspace() for char in fname) or len(fname.strip()) == 0:
            messages.warning(request, 'Invalid entry for first name')
            return redirect(profile)        

        if not all(char.isalpha() or char.isspace() for char in lname) or len(lname.strip()) == 0:
            messages.warning(request, 'Invalid entry for last name')
            return redirect(profile) 
        
        if not re.match(r'^[1-9]\d{9}$', number) or number.startswith('00'):
            messages.warning(request, 'Invalid entry for number')
            return redirect(profile)
        
        update_user = Account.objects.filter(id=user_id)  
        update_user.update(first_name=fname,last_name=lname,phone_number=number)
        return redirect(profile)
    

        
        if not re.match(r'^[1-9]\d{9}$', number) or number.startswith('00'):
            # If phone number is not valid, show error message
            error_message = 'Please enter a valid 10-digit phone number (not starting with 00)'
            return render(request, 'error.html', {'message': error_message})

    





    else:
        messages.info(request,'some field is empty')
        return render(request,'userpanel/profile.html',{'user':user})


# -----------------------------------------Banner_management-----------------------------------------
    
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

        if not description:
            messages.warning(request, 'Banner description shouldnt be empty')
            return redirect(banner_management)

        if not all(char.isalpha() or char.isspace() for char in name):
            messages.warning(request, 'Invalid entry for banner name')
            return redirect(banner_management)

        if not all(char.isalpha() or char.isspace() for char in description):
            messages.warning(request, 'Invalid entry for banner description')
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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        except OrderItem.DoesNotExist:
            messages.error(request, 'Something gone wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            




# -----------------------------------------Coupan management-----------------------------------------


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


login_required
def orders_list(request):

    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'cart/order_list.html', {'orders' : orders})




login_required
def order_details(request,order_id):
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
    except:
        pass 

    return render(request, 'cart/order_details.html', {'order_items' : order_items})




login_required
def order_tracking(request, item_id):
    current_date = timezone.now()
    item = OrderItem.objects.get(id=item_id)
    context = {
        'item' : item,
        'current_date' : current_date
    }
    return render(request, 'cart/order_tracking.html' ,context)


def order_invoice(request, order_id):

    order = Order.objects.get(id=order_id,user=request.user)

    order_items = OrderItem.objects.filter(order=order)


    context = {

        'order' : order,
        'order_items' : order_items
    }

    return render(request, 'cart/invoice.html',context)



def cancel_order(request, item_id=None, order_id=None):
        
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET_KEY))

    order = Order.objects.get(user=request.user, order_id=order_id)

    payment_id = order.payment.transaction_id

    item = OrderItem.objects.get(order=order, id=item_id)

    item_amount = int(item.item_total) * 100


    refund = client.payment.refund(payment_id,{'amount':item_amount})


    if refund is not None:

        item.order_status = 'Refunded'

        item.save()

        return render(request, 'orders/refund_success.html',{'order_id':order_id})
    
    else:

        return HttpResponse('Payment Not Captured')


# -----------------------------------------Order management admin side-----------------------------------------



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

