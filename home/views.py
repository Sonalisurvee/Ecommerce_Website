from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Banner
from account.models import Account,Address
from category.models import Category
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    dict_banner={
        'banners': Banner.objects.all().order_by('id'),
        'category': Category.objects.all().order_by('id')
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


def order_management(request):
    return render(request,'adminpanel/oredr_management.html')
