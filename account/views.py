from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
def log_in(request):
    return render(request,'userpanel/login.html')

def log_out(request):
    pass

def signup(request):
    return render(request,'userpanel/signup.html')


def otp(request):
    pass