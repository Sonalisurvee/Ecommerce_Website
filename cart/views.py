from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Cart,Cartitem
from django.core.exceptions import ObjectDoesNotExist


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
    product = Product.objects.get(id=product_id)

# thus try block is created just to chech wethere cart is ther or not ,once cart is created we are able to add produtc to it

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
        cart_item.save()
    except Cartitem.DoesNotExist:#if cart does not have any product then create one
        cart_item = Cartitem.objects.create(
            product=product,
            quantity=1,#as there is no product in cart quantity will be 1 as it is the first product in cart
            cart=cart
        )
        cart_item.save()
    return redirect('cart')




def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = Cartitem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')




def remove_cartitem(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product,id=product_id)
    cart_item = Cartitem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')




def cart(request, total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))#it will match the cart id with the session id to get the cart
        cart_items = Cartitem.objects.filter(cart=cart,is_active=True)# is_axtive used to indicate whether a user account is active or not.

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
    }    
    return render(request, 'cart/cart.html',context)




# -----------------------------------Carts --------------------------------



def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))#it will match the cart id with the session id to get the cart
        cart_items = Cartitem.objects.filter(cart=cart,is_active=True)# is_axtive used to indicate whether a user account is active or not.

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
    } 
    return render(request,'cart/checkout.html',context) 