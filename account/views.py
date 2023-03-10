from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import auth, User
from django.contrib import messages
from home.views import index
from .models import Account,Address

from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

from .forms import UserAddressForm

from django.conf import settings
from .models import UserOTP
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random

# -----------------------------------Accounts --------------------------------

@cache_control(no_cache=True,must_revalidate=True,no_store=True)        
def log_in(request):
#     if request.user.is_authenticated:
#         return redirect(index)
    if request.method == 'POST':
        email=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            if user.is_superadmin:
                 return render(request, 'adminpanel/admin_index.html')
            return redirect(index)
        else:
            messages.info(request,'Username or password is incorrect')
            return redirect(log_in)
    else:
        return render(request,'userpanel\login.html')
    
    
@cache_control(no_cache=True,must_revalidate=True,no_store=True)            
def log_out(request):
    auth.logout(request)            
    return redirect(log_in) 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)            
def signup(request):
     user = None
     if request.method == 'POST':
          get_otp = request.POST.get('otp')
          print(get_otp)

          #====OTP Verification===
          if get_otp:
               get_user = request.POST.get('user')
               user = Account.objects.get(username=get_user)
               otp_1 = UserOTP.objects.filter(user=user).last().otp
               print(user)
               print(get_otp)
               print(otp_1)
               if int(get_otp) == otp_1 :
                    user.is_active = True
                    user.save()
                    messages.success(request,f'Account created Successfully')
                    return redirect(log_in)
               else:
                    user.delete()
                    messages.warning(request,'You have entered a wrong OTP')
                    return render(request, 'userpanel/login.html',{'otp':True, 'user':user})

          # ===User registration====
          else:
               fname = request.POST['fname']
               lname = request.POST['lname']
               email = request.POST['email']
               number = request.POST['number']
               password1 = request.POST['password']
               password2 = request.POST['repassword']
               username  = email.split('@')[0]
          
          if fname and email and password1 and password2 and number != "":
               if password1 == password2:
                    if Account.objects.filter(email = email).exists():
                         messages.info(request,'Email already exists')
                         return redirect(signup)
                    elif Account.objects.filter(first_name = fname).exists():
                         messages.info(request,'Username already exists')
                         return redirect(signup)
                    else:
                         user = Account.objects.create_user(username=username, first_name=fname,last_name=lname,email=email,phone_number=number,password=password1)
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
     

# ------------------------------------Addresses --------------------------------


@login_required(login_url='/login')
def view_address(request):
     addresses = Address.objects.filter(customer=request.userr)
     # print(addresses)
     context = {
          'addresses': addresses,
     }
     return render(request,"userpanel/profile.html",context)


def add_address(request):
     if request.method == "POST":
          address_form = UserAddressForm(data=request.POST)
          if address_form.is_valid():
               address_form = address_form.save(commit=False)
               address_form.customer = request.user
               address_form.save()
               return HttpResponseRedirect(reverse("profile"))
     else:
          address_form = UserAddressForm()
     return render(request,"userpanel/address.html",{"form": address_form})


def edit_address(request,id):
     if request.method == "POST":
          address=Address.objects.get(pk=id,customer=request.user)
          address_form = UserAddressForm(instance = address,data=request.POST)
          if address_form.is_valid():
               address_form.save()
               return HttpResponseRedirect(reverse("profile"))
     else:
          address=Address.objects.get(pk=id,customer=request.user)
          address_form = UserAddressForm(instance = address)
     return render(request,"userpanel/address.html",{"form": address_form})
               
def delete_address(request,id):
    address=Address.objects.get(pk=id,customer=request.user).delete()
    return redirect("profile")
     
def default_address(request,id):
    Address.objects.get(customer=request,default=True).update(default=False)
    Address.objects.get(pk=id,customer=request).update(default=True)
    return redirect('profile')

