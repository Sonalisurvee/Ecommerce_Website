from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,SizeVariant
from .models import Coupon,Cartt,CartItems,Payment,Order,OrderItem
from account.models import Address
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
import razorpay
from django.conf import settings
from store.views import product_details

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
    
    if variation:
        variation = request.GET.get('variant')
        variant = SizeVariant.objects.get(size_name=variation)

    current_user = request.user
    product = Product.objects.get(id=product_id)
    if product.stock < 1:
        messages.warning(request, f"{product.product_name} are out of stock")
        return redirect('cart')

    
    if current_user.is_authenticated:
        cart , _ = Cartt.objects.get_or_create(user = current_user,is_paid = False)
        is_cart_item_exists = CartItems.objects.filter(carts=cart, products=product, size_variant=variant).exists()
        if is_cart_item_exists:
            cart_item = CartItems.objects.get(carts=cart, products=product, size_variant=variant)
            if cart_item.quantity >= product.stock:
                messages.info(request,f"Sorry, only {product.stock} units of {product.product_name} are available.")
                return redirect('cart')
                # return False, f"Sorry, only {product.stock} units of {product.product_name} are available."
            else:
                cart_item.quantity+=1
        else:
            cart_item = CartItems.objects.create( 
            carts = cart,
            products=product,
            size_variant = variant
        )
        cart_item.save()

    else:
        try:   
            cart = Cartt.objects.get(cart_id=_cart_id(request))
        except Cartt.DoesNotExist: 
            cart = Cartt.objects.create(cart_id=_cart_id(request)) 
        cart.save()
        try:
            cart_item = CartItems.objects.get(products=product,carts=cart,size_variant=variant)
            cart_item.quantity+=1 
        except CartItems.DoesNotExist:
            cart_item = CartItems.objects.create(
                products=product,
                carts=cart,
                size_variant=variant
            )
        cart_item.save() 
    messages.success(request, f"{product.product_name}Item had been added to the cart")  
    return redirect('cart')


def remove_cartt(request,product_id,cart_item_id):
    product = get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItems.objects.get(products=product,id=cart_item_id)    
        else:
            cart = Cartt.objects.get(cart_id=_cart_id(request))
            cart_item = CartItems.objects.get(products=product,carts=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cartitems(request,product_id,cart_item_id):    
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItems.objects.get(products=product,id=cart_item_id)
    else:
        cart = Cartt.objects.get(cart_id=_cart_id(request))
        cart_item = CartItems.objects.get(products=product,carts=cart,id=cart_item_id)
    cart_item.delete()
    messages.success(request, f"{product.product_name} has been removed from the cart")
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


# KEY = 'rzp_test_a0WKFGxNpEjkyL'
# SECRET_KEY = 'k7q1VWdctZVX6sZe9p9FWGpJ'


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
        

        # if name

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
            client = razorpay.Client(auth = (settings.KEY , settings.SECRET_KEY))
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
        

def success(request):
    order_id = request.GET.get('order_id')
    cart = Cartt.objects.get(razorpay_order_id = order_id )

    # razorpay_order_id = request.GET.get('razorpay_order_id').split("_")[1]
    # cart = Cartt.objects.get(razorpay_order_id=razorpay_order_id )


# this will create details in the payment model 

    current_user = request.user
    transaction = request.GET.get('order_id')
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

        orderitems.products.stock -= orderitems.quantity

        orderitems.products.save()

        order_items = OrderItem.objects.create(
            user = current_user,
            order =orders ,
            product = orderitems.products,
            item_price = orderitems.get_product_price(),
            quantity = orderitems.quantity,
            item_total = orderitems.sub_total()
        )    
        order_items.save()
        if orderitems.size_variant:
            order_items.variant = orderitems.size_variant.size_name
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



# ------------------------------------------------------order_success ---------------------------------------------------


def order_confirmation(request):
    return render(request,'cart/order_confirmation.html')


# -----------------------------------------Order management user side-----------------------------------------

