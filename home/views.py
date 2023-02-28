from django.shortcuts import render,redirect
from.models import Banner

# Create your views here.
def index(request):
    dict_banner={
        'banners': Banner.objects.all().order_by('id')
    }    
    return render(request,'userpanel/index.html',dict_banner)
