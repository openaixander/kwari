from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.urls import reverse

from .forms import OrderCreateForm
from cart.cart import Cart
from services.paystack_service import PaystackService
from .models import Order,OrderItem
from django.contrib.auth.decorators import login_required
from products.models import Product
# Create your views here.

# I did not create the OrderCreateForm for that will be given by you to help create it

@login_required(login_url='accounts:login')
def checkout_view(request):

    cart = Cart(request)

    if len(cart) == 0 :
        return redirect('products:product_list')
    

    if request.method == 'POST':
        
        form = OrderCreateForm(request.POST)
        
        if form.is_valid():
            try:
                # START ENTERPRISE TRANSACTION BLOCK
                with transaction.atomic():
                    # 1. Create the Envelope (Order)
                    order = form.save(commit=False)
                    order.user = request.user
                    order.save()

                    # 2. Process Items Safely
                    for item in cart:
                        # THE LOCK: select_for_update() locks this specific product row until the order is done
                        product = Product.objects.select_for_update().get(id=item['product'].id)

                        # 3. Double-check stock (in case it sold out while they were in the checkout page)
                        if product.stock >= item['quantity']:
                            # Deduct stock and save
                            product.stock -= item['quantity']
                            product.save()

                            # Create the receipt
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                price=item['price'],
                                quantity=item['quantity']
                            )
                        else:
                            # If stock ran out, abort the entire transaction!
                            raise Exception(f"Sorry, {product.name} just sold out or doesn't have enough stock.")
                    
                    amount = order.get_total_cost()

                    callback_url = request.build_absolute_uri(reverse('orders:verify_payment'))

                    payment_response = PaystackService.initialize_payment(
                        email=request.user.email,
                        amount=amount,
                        order_id=order.id,
                        callback_url=callback_url
                    )

                    if payment_response['status'] is True:
                        payment_url = payment_response['data']['authorization_url']
                        return redirect(payment_url)
                    else:
                        raise Exception('Payment Gateway Error. Please try again')

            except Exception as e:
                # Catch the "out of stock" error, display it, and send them back to the cart
                messages.error(request, str(e))
                return redirect('cart:cart_detail')
        else:
            messages.error(request, "Please correct the errors in the form below.")
            
    else:
        # CLEAN GET REQUEST: Pre-fill the data
        form = OrderCreateForm(initial={
            'full_name': request.user.display_name
        })
    
    context = {
        'cart': cart,
        'form': form
    }
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='accounts:login')
def verify_payment_view(request):
    reference = request.GET.get('reference')

    if not reference:
        return redirect('products:product_list')
    
    response = PaystackService.verify_payment(reference)


    if response['status'] is True and response['data']['status'] == 'success':
        # payment was completly successful

        order_id = reference.split('-')[-1]
        order = get_object_or_404(Order, id=order_id)


        order.is_paid = True
        order.save()

        # Now we clear the cart
        cart = Cart(request)
        cart.clear()

        return redirect("orders:checkout_success")
    else:
        messages.error(request, "Payment failed or was cancelled")
        return redirect("cart:cart_detail")

@login_required(login_url='accounts:login')
def checkout_success_view(request):
    
    return render(request, 'orders/success.html')

        
@login_required(login_url='accounts:login')
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'orders/order_detail.html', context={'order':order})


