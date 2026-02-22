from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from products.models import Product
from .cart import Cart
from django.views.decorators.http import require_POST

# Create your views here.

@require_POST
def cart_add(request, product_id):
    """ This is what takes the products and it is then add to the cart """
    cart = Cart(request)

    # get the product
    product = get_object_or_404(Product, id=product_id)


    # Get quantity (default to 1)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    # Check if this is an override (update) or an add
    override = request.POST.get('override_quantity', False)
    
    # CALL THE BRAIN
    added = cart.add(product=product, quantity=quantity, override_quantity=override)

    # HANDLE AJAX REQUESTS (listing page)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if added:
            return JsonResponse({
                'success': True, 
                'cart_total': len(cart), 
                'message': 'Added to cart'
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Out of stock'
            }, status=400)

    # HANDLE STANDARD REQUESTS (detail page)
    if not added:
        # Ideally, use Django Messages here to say "Out of stock"
        pass 
        
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)


    cart.remove(product)

    return redirect('cart:cart_detail')


def cart_detail(request):
    # initialize the Cart
    cart = Cart(request)

    context = {
        'cart': cart
    }
    return render(request, 'cart/cart_detail.html', context)

