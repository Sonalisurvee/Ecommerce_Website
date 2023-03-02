from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import auth, User
from django.contrib import messages
from home.views import index
from .models import Account

from django.conf import settings
from .models import UserOTP
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random

# Create your views here.

def log_in(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect(index)
        else:
            messages.info(request,'Username or password is incorrect')
            return redirect(log_in)
    else:
        return render(request,'userpanel\login.html')

def log_out(request):
    auth.logout(request)            
    return redirect(log_in) 


def signup(request):
     user = None
     if request.method == 'POST':
          get_otp = request.POST.get('otp')

          #====OTP Verification===
          if get_otp:
               get_user = request.POST.get('user')
               user = Account.objects.get(username=get_user)
               if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                    user.is_active = True
                    user.save()
                    messages.success(request,f'Account created Successfully')
                    return redirect(log_in)
               else:
                    user.delete()
                    messages.warning(request,'You have entered a wrong OTP')
                    return render(request, 'userpanel/signup.html',{'otp':True, 'user':user})

          # ===User registration====
          else:
               username = request.POST['username']
               email = request.POST['email']
               password1 = request.POST['password']
               password2 = request.POST['repassword']
          
          if username and email and password1 and password2 != "":
               if password1 == password2:
                    if Account.objects.filter(email = email).exists():
                         messages.info(request,'Email already exists')
                         return redirect(signup)
                    elif Account.objects.filter(username = username).exists():
                         messages.info(request,'Username already exists')
                         return redirect(signup)
                    else:
                         user = Account.objects.create_user(username=username,email=email,password=password1,first_name='Any',last_name='Name')
                         user.set_password(password1)
                         user.is_active = False
                         user.save()
                         user_otp = random.randint(1000,9999)
                         UserOTP.objects.create(user=user,otp=user_otp)
                         mess=f'Hello\t{user.username},\nYour OTP for the Account Verfication for Signora is {user_otp}\nThank You!'
                         send_mail(
                              "Welcome to Signora.Verify Your Account",
                              mess,
                              settings.EMAIL_HOST_USER,
                              [user.email],
                              fail_silently=False,
                         )
                         return render(request,'userpanel/otp.html',{'otp':True, 'user':user})
               else:
                    messages.info(request,"Password doesn't match")
                    return redirect(signup)
          else:
               messages.info(request,"Some fields are empty")
               return redirect(signup)
     else:
          return render(request,'userpanel/signup.html')




