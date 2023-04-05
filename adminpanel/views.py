from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.contrib import messages
from home.models import Admin_profile
from account.models import Account
from cart.models import Coupon,Order,OrderItem
from store.models import ReviewRating
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

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
   


# -----------------------------------------------review management-----------------------------------------------

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



# -----------------------------------------------Admin profile----------------------------------------------

@login_required(login_url='/login')
def admin_profile(request):
        admin = Admin_profile.objects.get(user = request.user)


        # profile = Account
        return render(request,'adminpanel/admin_profile.html',{'admin': admin})

@login_required(login_url='/login')
def admin_profile_update(request,admin_id):
    
        return render(request,'adminpanel/admin_profile.html')
    