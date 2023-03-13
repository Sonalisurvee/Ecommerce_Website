from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Cart,Cartitem,Coupon
from account.models import Address
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# -----------------------------------Carts --------------------------------

# this is a private method where our session id is stored
def _cart_id(request):
    cart = request.session.session_key
# if the session is not present then it will create new session
    if not cart:
        cart = request.session.create()
    return cart
 

#this cart id fun is created just assign our cart the session id ,wen log in there session id will be created and every userhas its own unqiue 
# session id so every user will have its own cart so no one can have our cart items ,privacy will be maintained.



def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

# thus try block is created just to chech wethere cart is ther or not ,once cart is created we are able to add produtc to it
    if current_user.is_authenticated:
    
        is_cart_item_exists = Cartitem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = Cartitem.objects.get(product=product,user=current_user)
            cart_item.quantity+=1 #incrementing the quantity of prodiuct presnet in the cart
        else:
            cart_item = Cartitem.objects.create( #if not exist it will create one cart
            product=product,
            user = current_user,
            quantity = 1
        )
        cart_item.save()
    
    # If user is not authenticated
    else:

        try:
            
            cart = Cart.objects.get(cart_id=_cart_id(request))
            # cart_id=_cart_id(request),means it will assign cart id as with the session id or key and if cart does not exsit it will go y-to except condi
            #it will match the cart id with the session id to get the cart,lile if we dint add any product in the cart the cart will be emoty ryt 
            # so we nend to check whether that cart exists or not so we gave try and except here.

        except Cart.DoesNotExist: #wat if cart does not exist
            cart = Cart.objects.create( #if not exist it will create one cart
                cart_id=_cart_id(request)
            )
        cart.save()

        # this try block is created to add products in cart

        try:
            cart_item = Cartitem.objects.get(product=product,cart=cart)
            cart_item.quantity+=1 #incrementing the quantity of prodiuct presnet in the cart
        except Cartitem.DoesNotExist:#if cart does not have any product then create one
            cart_item = Cartitem.objects.create(
                product=product,
                quantity=1,#as there is no product in cart quantity will be 1 as it is the first product in cart
                cart=cart
            )
        cart_item.save()
    return redirect('cart')




def remove_cart(request,product_id,cart_item_id):
    product = get_object_or_404(Product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = Cartitem.objects.get(product=product,user=request.user,id=cart_item_id)
    
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = Cartitem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')




def remove_cartitem(request,product_id,cart_item_id):    
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
        cart_item = Cartitem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cartitem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')




def cart(request, total=0,quantity=0,cart_items=None):
     
    
    try:
        print('Loading')
        if request.user.is_authenticated:#fro login users
            cart_items = Cartitem.objects.filter(user=request.user,is_active=True)
        else:#fro not login 
            print("inside esle ")
            cart = Cart.objects.get(cart_id=_cart_id(request))#it will match the cart id with the session id to get the cart
            cart_items = Cartitem.objects.filter(cart=cart,is_active=True)# is_axtive used to indicate whether a user account is active or not.
            print("else will end")
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total =  total + tax
    except ObjectDoesNotExist:
        print("Cart item does not exist")
        pass         

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }    
    return render(request, 'cart/cart.html',context)



# ------------------------------------------------------Checkout ---------------------------------------------------


@login_required(login_url= 'log_in')
def checkout(request,total=0,quantity=0,cart_items=None):
    addresses = Address.objects.filter(customer=request.user)
    name=Address.objects.filter(default=True)
    current_user = request.user

# thus try block is created just to chech wethere cart is ther or not ,once cart is created we are able to add produtc to it
    if current_user.is_authenticated:
        try:
            cart_items = Cartitem.objects.filter(user=current_user,is_active=True)# is_axtive used to indicate whether a user account is active or not.
            total = 0
            quantity = 0
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total)/100            
            grand_tot = total + tax
        except ObjectDoesNotExist:
            pass

         # -----------------Coupon-----------------

        # if request.method == 'POST':
        #     print("coupon if")
        #     coupon = request.POST.get('coupon')
        #     coupon_obj = Coupon.objects.filter(coupan_code__icontains = coupon)
        #     print('hello')
        #     print(coupon_obj)
        #     print('jjjj')          
            
        #     if not coupon_obj.exists():
        #         print('in valiud')
        #         messages.warning(request, 'in valid coupon')
        #         return redirect(checkout)
            
        #     if cart_item.coupon:# checking wether cartitem table has coupon or not ,coupon exists or not
        #         print('coupan exit')
        #         messages.warning(request, 'coupon already exists')
        #         return redirect(checkout)       
                  

        #     for cart_itemm in cart_items:
        #         total += (cart_itemm.product.price * cart_itemm.quantity)
        #         quantity += cart_itemm.quantity
        #         grand_tot = total - coupon_obj.discount_price

        #     # print(f"cart_item: {cart_item}")
        #     # print(f"grand_total: {cart_item.grand_total()}")
       
        #     if grand_tot > coupon_obj.first().minimum_amount:
        #         messages.warning(request, f"Amount should be greater than {coupon_obj.first().minimum_amount}")
        #         return redirect(checkout)

        if request.method == 'POST':
            coupon = request.POST.get('coupon')
            coupon_obj = Coupon.objects.filter(coupan_code__icontains = coupon)

            if not coupon_obj.exists():
                messages.warning(request, 'Invalid coupon')
                return redirect(checkout)

            if cart_item.coupon:
                messages.warning(request, 'Coupon already exists')
                return redirect(checkout)

            # for cart_itemm in cart_items:
            #     total = (cart_itemm.product.price * cart_itemm.quantity)
            #     quantity = cart_itemm.quantity
            #     grand_tot = total - coupon_obj[0].discount_price
            #     print(cart_itemm.product.price)
            #     print(cart_itemm.quantity)
            #     print(total,'one')
            #     print(quantity,'two')
            #     print(grand_tot,'dfghj')

            if grand_tot < coupon_obj[0].minimum_amount:
                messages.warning(request, f"Amount should be greater than {coupon_obj[0].minimum_amount}")
                return redirect(checkout)
                        
            if coupon_obj[0].is_expired:
                messages.warning(request, 'Coupan had been expired')
                return redirect(checkout)                


            cart_item.coupon = coupon_obj[0]#both if statement ontop fails then coupon_obj will get stored in cart_item.coupan,[0]?
            print(cart_item)
            cart_item.save()    
            messages.success(request,'coupan applied')
            return redirect(checkout)  
        
         # -----------------Coupon-end----------------
                  
        if cart_item.coupon:
            grand_tot = (total - cart_item.coupon.discount_price) + tax

        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,  
            'cart_item':cart_item,  
            'user_addresses': addresses,
            'name':name,
            'grand_tot':grand_tot,
            'tax':tax
        }
    else:
        pass 


    return render(request,'cart/checkout.html',context) 


def remove_coupan(request,cart_id):
    cart = Cartitem.objects.get(id=cart_id)
    cart.coupon = None
    cart.save()
    messages.success(request,'coupan removed')
    return redirect(checkout) 
    

# ------------------------------------------------------order_success ---------------------------------------------------



def order_success(request):
    return render(request,'cart/order_success.html') 
