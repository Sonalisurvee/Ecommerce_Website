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



def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        #it will match the cart id with the session id to get the cart
    except Cart.DoesNotExist: #wat if cart does not exist
        cart = Cart.objects.create( #if not exist it will create one cart
            cart_id=_cart_id(request)
        )
    cart.save()

    # to add product in cart

    try:
        cart_item = Cartitem.objects.get(product=product,cart=cart)
        cart_item.quantity+=1 #incrementing the quantity of prodiuct presnet in the cart
        cart_item.save()
    except Cartitem.DoesNotExist:#if cart does not have any product thn create one
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
        cart = Cart.objects.get(cart_id=_cart_id(request))#it will match the cart id with the session id t get the cart
        cart_items = Cartitem.objects.filter(cart=cart,is_active=True)
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