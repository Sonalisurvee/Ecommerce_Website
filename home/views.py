from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import auth, User
from .models import Banner
from account.models import Account

# Create your views here.
def index(request):
    dict_banner={
        'banners': Banner.objects.all().order_by('id')
    }    
    return render(request,'userpanel/index.html',dict_banner)


def admin_index(request):
    return render(request,'adminpanel/admin_index.html')

def user_management(request):
    dict_user={
        'users':User.objects.all().order_by('id')
    }    
    return render(request,'adminpanel/user_management.html',dict_user)


def block_unblock(request,user_id):
    user=get_object_or_404(User,id=user_id) #is user that we are checking exits then it will store it in the user variable else it will throw man 404 error
    if user.is_active:
        user.is_active=False#just converting the active status of the user to inaction
        user.save()
        return redirect(user_management)
    else:
        user.is_active=True
        user.save()
        return redirect(user_management)


def profile(request):

    if Account.objects.get(username='ck'):
        dict={
            'account': Account.objects.get(username='ck')
        }
        return render(request,'userpanel/profile.html',dict)
    else:
        return render(request,'userpanel/profile.html')


def error_404(request,exception):
    return render(request,'404.html')