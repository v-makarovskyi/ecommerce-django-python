import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from account.models import Address
from cart.cart import Cart


from .models import DeliveryOptions

@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, 'checkout/delivery_choices.html', {'deliveryoptions': deliveryoptions})


@login_required
def cart_update_delivery(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        delivery_option = int(request.POST.get('deliveryoption'))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        update_total_price = cart.cart_update_delivery(delivery_type.delivery_price)

        session = request.session
        if 'purchase' not in request.session:
            session['purchase'] = {'delivery_id': delivery_type.id}
        else:
            session['purchase']['delivery_id'] = delivery_type.id
            session.modified = True
        
        response = JsonResponse({'total': update_total_price, 'delivery_price': delivery_type.delivery_price})
        return response


@login_required
def delivery_address(request):
    session = request.session
 

    if 'purchase' not in request.session:
        messages.success(request, 'Пожалуйста, выберите вариант доставки')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    addresses = Address.objects.filter(customer=request.user).order_by('-default')
    
    if 'address' not in request.session:
        session['address'] = {'address_id': str(addresses[0].id)}
    else:
        session['address']['address_id'] = str(addresses[0].id) 
        session.modified = True

    return render(request, 'checkout/delivery_address.html', {'addresses': addresses})
    

@login_required
def payment_selection(request):

    session = request.session
    if 'address' not in session:
        messages.success(request, 'Пожалуйста, выберите актуальный адрес доставки')
        return HttpResponseRedirect(request.MTA['HTTP_REFERER'])
    
    return render(request, 'checkout/payment_selection.html', {})

@login_required
def payment_successful(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "checkout/payment_successful.html", {})






