from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Banner
from account.models import Account,Address
from category.models import Category
from cart.models import Coupon
from store.models import Product
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


def index(request):   
    banners = Banner.objects.all().order_by('id')
    category = Category.objects.all().order_by('id')

    dict_banner={
        'banners': banners,
        'category': category,

    }    
    return render(request,'userpanel/index.html',dict_banner)


@login_required(login_url='/login')
def admin_index(request):
    if request.user.is_authenticated and request.user.is_superadmin:
        return render(request, 'adminpanel/admin_index.html')
    else:
        return redirect('/')


# -----------------------------------------user_management-----------------------------------------


def user_management(request):
    dict_user={
        'users':Account.objects.all().order_by('id')
    }    
    return render(request,'adminpanel/user_management.html',dict_user)


def block_unblock(request,user_id):
    user=get_object_or_404(Account,id=user_id) #is user that we are checking exits then it will store it in the user variable else it will throw man 404 error
    if user.is_active:
        user.is_active=False#just converting the active status of the user to inaction
        user.save()
        return redirect(user_management)
    else:
        user.is_active=True
        user.save()
        return redirect(user_management)


# -----------------------------------------user_profile-----------------------------------------


@login_required(login_url='/login')
def profile(request):
    context = {
        'user_addresses': Address.objects.filter(customer=request.user)
    }
    return render(request, 'userpanel/profile.html',context)



#---
def update_profile(request,user_id):
    user=get_object_or_404(Account,pk=user_id)
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        number=request.POST['number']            
        update_user = Account.objects.filter(id=user_id)  
        update_user.update(first_name=fname,last_name=lname,phone_number=number)
        return redirect(profile)

    else:
        messages.info(request,'some field is empty')
        return render(request,'userpanel/profile.html',{'user':user})


# -----------------------------------------Banner_management-----------------------------------------

def banner_management(request):
    dict_banner={
        'banners': Banner.objects.all().order_by('id'),
    }    
    return render(request,'adminpanel/banner_management.html',dict_banner)

def banner_delete(request,banner_id):
    delet_banner = Banner.objects.filter(id=banner_id)   
    delet_banner.delete()
    return redirect(banner_management)

def banner_edit(request,banner_id):
    banner=get_object_or_404(Banner,pk=banner_id)
    if request.method=='POST':
        name=request.POST['name']
        description=request.POST['description']
        discount=request.POST['discount']

        if int(discount) < 0:
            messages.info(request,"Negative values are not allowed.")
            return redirect(banner_management)

        try:
            update_banner=Banner.objects.get(id=banner_id)
            image=request.FILES['image']
            update_banner.banner_image=image
            update_banner.save()
        except:
            pass

        update_banner=Banner.objects.filter(id=banner_id)
        update_banner.update(banner_name=name,note=description,discount=discount)
        return redirect(banner_management)
    else:
        messages.info(request,'some field is empty')
        return render(request,'adminpanel/banner_management.html',{'banner':banner})
    

# -----------------------------------------404-----------------------------------------


def error_404(request,exception):
    return render(request,'404.html')


# -----------------------------------------Order management-----------------------------------------


def order_management(request, order_id=0):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        status = request.POST['order_status']
        order.status = status
        order.save()
        return redirect(order_management) 

    dict_order = {
        'order': Order.objects.all().order_by('id'),
        'statuses' : Order.orderstatuses
    }
    return render(request,'adminpanel/order_management.html',dict_order)



# -----------------------------------------Coupan management-----------------------------------------


def coupan_management(request):
    dict_coupon = {
        'coupon':Coupon.objects.all().order_by('id')
    }
    return render(request,'adminpanel/coupan_management.html',dict_coupon)


def delete_coupon(request,coupan_id):
    del_record = Coupon.objects.filter(id=coupan_id)
    del_record.delete()
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
        
        if int(minimum) < 0 or int(discount) < 0 :
            messages.info(request,"Negative values are not allowed.")
            return redirect(coupan_management)

     
        if Coupon.objects.filter(coupan_code=coupon).exists():
            messages.info(request,"This coupon already exists")
            return redirect(coupan_management)
            
        else:
            update_coupon = Coupon.objects.filter(id=coupan_id)  
            update_coupon.update(coupan_code=coupan,discount_price=discount,minimum_amount=minimum)
            return redirect(coupan_management)
        
        

    else:
        messages.info(request,'some field is empty')
        return render(request,'adminpanel/coupan_management.html')
    

def add_coupon(request):
    if request.method == 'POST':
        couponn = request.POST['coupon']
        discount = request.POST['discount']
        minimum=request.POST['minimum'] 

        if int(minimum) < 0 or int(discount) < 0 :
            messages.info(request,"Negative values are not allowed.")
            return redirect(coupan_management)

        if Coupon.objects.filter(coupan_code=couponn).exists():
            messages.info(request,"This coupon already exists")
            return redirect(coupan_management)
        else:
            coupan = Coupon.objects.create(coupan_code=couponn,discount_price=discount,minimum_amount=minimum)
            coupan.save()           
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



# def orders(request):


#     return render(request,'new.html')
