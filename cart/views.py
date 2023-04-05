from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,SizeVariant,Varitaion
from .models import Coupon,Cartt,CartItems,Payment,Order,OrderItem
from account.models import Address
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
import razorpay
from django.conf import settings
from store.views import product_details
from django.http import JsonResponse

# -----------------------------------Carts --------------------------------

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
        print('created cart id', cart)
    return cart 


def add_to_cart(request,product_id):
    variant = None
    variation =None
    variation = request.GET.get('variant')#querystring
    product = Product.objects.get(id=product_id)
    
    if variation:
        variation = request.GET.get('variant')
        size = SizeVariant.objects.get(size_name=variation)
        variant = Varitaion.objects.get(product=product, size_variant=size)


    current_user = request.user
    if variant.stock < 1:
        messages.warning(request, f"{product.product_name} are out of stock")
        return redirect('cart')

    
    if current_user.is_authenticated:
        cart , _ = Cartt.objects.get_or_create(user = current_user,is_paid = False)
        is_cart_item_exists = CartItems.objects.filter(carts=cart, products=product, variant=variant).exists()
        if is_cart_item_exists:
            cart_item = CartItems.objects.get(carts=cart, products=product, variant=variant)
            if cart_item.quantity == variant.stock:
                messages.info(request,f"Sorry, only {variant.stock} units of {product.product_name} are available.")
                return redirect('cart')
            cart_item.variant = variant
            cart_item.quantity += 1
        else:
            cart_item = CartItems.objects.create( 
            carts = cart,
            products=product,
            variant = variant
        )
        cart_item.save()

    else:
        try:   
            cart = Cartt.objects.get(cart_id=_cart_id(request))
        except Cartt.DoesNotExist: 
            cart = Cartt.objects.create(cart_id=_cart_id(request)) 
        cart.save()
        try:
            cart_item = CartItems.objects.get(products=product,carts=cart,variant=variant)
            if cart_item.quantity == variant.stock:
                messages.info(request,f"Sorry, only {variant.stock} units of {product.product_name} are available.")
                return redirect('cart')
            cart_item.variant = variant
            cart_item.quantity += 1
        except CartItems.DoesNotExist:
            cart_item = CartItems.objects.create(
                products=product,
                carts=cart,
                variant=variant
            )
        cart_item.save() 
    messages.success(request, f"{product.product_name}Item had been added to the cart")  
    return redirect('cart')



def cart(request):
    cart=None
    cart_items=None
    try:
        if request.user.is_authenticated:
            cart, _ = Cartt.objects.get_or_create(user=request.user, is_paid = False)
            cart_items = CartItems.objects.filter(carts=cart).order_by('id')
        else:
            cart = Cartt.objects.get(cart_id=_cart_id(request))
            cart_items = CartItems.objects.filter(carts=cart).order_by('id')
       
    except Exception as e:
        pass

    context = {
        'cart':cart,
        'cart_items':cart_items,
    
    }    
    return render(request, 'cart/cartt.html',context)


# ----------------------------------checkout--------------------------------------------


# @login_required(login_url= 'log_in')
def checkout(request,cart_items=None):
    if request.user.is_authenticated:
        cart = None
        addresses = Address.objects.filter(customer=request.user).order_by('id')
        name=Address.objects.filter(default=True)
        current_user = request.user

    # thus try block is created just to chech wethere cart is ther or not ,once cart is created we are able to add produtc to it
        context = {}
        try:
            cart = Cartt.objects.get(user=current_user, is_paid=False)
            cart_items = CartItems.objects.filter(carts=cart)
            
        except:
            pass
    

        if request.method == 'POST':
            coupon = request.POST.get('coupon')
            coupon_obj = Coupon.objects.filter(coupan_code__icontains = coupon)

            if not coupon_obj.exists():
                messages.warning(request, 'The promo code you have entered is invalid. PLease try again')
                return redirect(checkout)

            if cart.coupon:
                messages.warning(request, 'Coupon already exists')
                return redirect(checkout)


            if cart.get_cart_total() < coupon_obj[0].minimum_amount:
                messages.warning(request, f"Amount should be greater than {coupon_obj[0].minimum_amount}")
                return redirect(checkout)
                        
            if coupon_obj[0].is_expired:
                messages.warning(request, 'Coupan had been expired')
                return redirect(checkout)                


            cart.coupon = coupon_obj[0]#both if statement ontop fails then coupon_obj will get stored in cart_item.coupan,[0]?
            cart.save()  
            messages.success(request,'coupan applied')
            return redirect(checkout)  
        
            # -----------------Coupon-end----------------
        try:
            client = razorpay.Client(auth = (settings.KEY_ID , settings.KEY_SECRET))
            payment = client.order.create({'amount' : int(cart.get_grand_total()) * 100, 'currency' : 'INR', 'payment_capture': 1})
            cart.razorpay_order_id = payment['id']
            cart.save()

        except:
            pass  
        
        coup = Coupon.objects.filter(is_expired = False)
        context = {       
            'cart_items':cart_items,  
            'cart':cart,  
            'user_addresses': addresses,
            'name':name,
            'payment':payment,
            'coupon':coup
        }
        return render(request,'cart/checkout.html',context) 
    else:
        messages.warning(request, 'Login required to checkout')
        return redirect('log_in')
    
    
# referer = request.META['HTTP_REFERER']
# return HttpResponseRedirect(referer)
        

def success(request):
    order_id = request.GET.get('order_id')
    cart = Cartt.objects.get(razorpay_order_id = order_id )

# this will create details in the payment model 

    current_user = request.user
    transaction = request.GET.get('razorpay_payment_id')
    cart_total = cart.get_cart_total()
    tax =cart.get_tax()
    grand_total = cart.get_grand_total()
    payment = Payment.objects.create(
        user =current_user,
        transaction_id = transaction,
        cart_total = cart_total,
        tax = tax,
        grand_total = grand_total,
    )
    payment.save() 

# this will create orders in the order model

    address = Address.objects.get(customer=request.user,default=True)    
    orders = Order.objects.create(
        order_id = order_id,
        user = current_user ,
        delivery_address = address ,
        payment = payment ,
    )

# this will store the products in the orderItem model
# here orderitems.products and rest is taken from the cartitems model because the products are in the cartitesm now 

    order_items = CartItems.objects.filter(carts = cart)
    for orderitems in order_items:

        orderitems.variant.stock -= orderitems.quantity

        orderitems.variant.save()

        order_items = OrderItem.objects.create(
            user = current_user,
            order =orders ,
            product = orderitems.products,
            item_price = orderitems.get_product_price(),
            quantity = orderitems.quantity,
            item_total = cart.get_grand_total()
            # get_grand_total
        )    
        order_items.save()
        if orderitems.variant.size_variant:
            order_items.variant = orderitems.variant.size_variant.size_name 
            order_items.save()

            order_items.variantion = orderitems.variant
            order_items.save()

    # Deleting the cart once we haev ordered the product

    cart.is_paid = True
    cart.delete()
    return render(request, 'cart/order_success.html', {'order_id': order_id})


def remove_coupon(request):
    try:
        cart = Cartt.objects.get(user=request.user, is_paid=False)
        cart.coupon = None
        cart.save()
        messages.success(request, 'Coupon removed successfully')
    except:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





# after ajax

def cart_delete(request):


    if request.POST.get('action') == 'post':

        item_id = int(request.POST.get('item_id'))
        item = CartItems.objects.get(id = item_id)
        item.delete()
        
        response = JsonResponse({"message":'success'})
        return response


def cart_update(request):

    # cart = Cart_session(request)
    if request.POST.get('action') == 'post':

        if request.user.is_authenticated:

            item_id = int(request.POST.get('item_id'))
            product_quantity = int(request.POST.get('product_quantity'))

            # cart.update(variant=variant_id, qty=product_quantity)
        
            print('item id = ',item_id,'quatity = ',product_quantity)

            item = CartItems.objects.get(id=item_id )
            item.quantity = product_quantity
            item.save()

            cart_id = item.carts.id
            cart_obj = Cartt.objects.get(id=cart_id)            
            cart_gst = cart_obj.get_tax()
            cart_total = cart_obj.get_cart_total()
            single_product_total = item.sub_total()
            grand_total = cart_total + cart_gst

            print(cart_gst,' ', cart_total,' ', grand_total)

            response = JsonResponse({'single_product_total':single_product_total,'sub_total':cart_total, 'gst':cart_gst, 'grand_total':grand_total})
            return response 
        
        else:            
            item_id = int(request.POST.get('item_id'))
            product_quantity = int(request.POST.get('product_quantity'))

            # cart.update(variant=variant_id, qty=product_quantity)
        
            print('item id = ',item_id,'quatity = ',product_quantity)

            item = CartItems.objects.get(id=item_id )
            item.quantity = product_quantity
            item.save()

            cart_id = item.carts.id

            try:   
                cart_obj = Cartt.objects.get(cart_id=_cart_id(request))
            except Cartt.DoesNotExist: 
                cart_obj = Cartt.objects.create(cart_id=_cart_id(request)) 
            cart_obj.save()
            
            # cart_obj = Cartt.objects.get(id=cart_id)    
                    
            cart_gst = cart_obj.get_tax()
            cart_total = cart_obj.get_cart_total()
            single_product_total = item.sub_total()
            grand_total = cart_total + cart_gst

            print(cart_gst,' ', cart_total,' ', grand_total)

            response = JsonResponse({'single_product_total':single_product_total,'sub_total':cart_total, 'gst':cart_gst, 'grand_total':grand_total})
            return response