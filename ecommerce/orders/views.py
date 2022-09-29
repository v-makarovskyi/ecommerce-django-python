from contextlib import redirect_stderr
from decimal import Decimal
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from cart.cart import Cart


from .models import Order
from account.models import Address


def add(request):
    user_id = request.user.id
    email = request.user.email

    addresses = Address.objects.filter(customer=user_id).order_by('default')

    for address in addresses:
        full_name = address.full_name
        address1 = address.address_line
        address2 = address.address_line2
        city = address.town_city
        phone = address.phone
        postal_code = address.postcode

    cart = Cart(request)
    
    carttotal = cart.get_total_price() 
    
    for item in cart:
        quantity = item['qty']
        product = item['product']
        price = item['price']
    
    order = Order.objects.create(
        user_id=user_id,
        email=email,
        full_name=full_name,
        address1=address1,
        address2=address2,
        phone=phone,
        postal_code=postal_code,
        city=city,
        quantity=quantity,
        price=price,
        product=product,
        total_paid=carttotal
    )

    return redirect('checkout:payment_successful')


@login_required
def payment_successful(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "checkout/payment_successful.html", {})
