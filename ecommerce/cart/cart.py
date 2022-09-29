from decimal import Decimal

from django.conf import settings
from catalogue.models import Product
from checkout.models import DeliveryOptions


class Cart:
    """ The base class of a cart that defines some default behaviors. 
    These options can be inherited or overridden. """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, qty):
        """ Adding and updating the users basket session data """

        product_id = str(product.id)
        print(product_id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        else:
            self.cart[product_id] = {'price': str(
                product.regular_price), 'qty': qty}

        self.save()

    def __iter__(self):
        """Accumulates product IDs in the session data in order to access the database to get products"""

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
    
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """Get the cart data and count the qty of items"""
        return sum(item['qty'] for item in self.cart.values())

    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        self.save()

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())


    def get_delivery_price(self):
        newprice = 0.00

        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(
                id=self.session['purchase']['delivery_id']).delivery_price

        return newprice
        

    def get_total_price(self):
        newprice = 0.00
        subtotal = sum(Decimal(item['price']) * item['qty']
                       for item in self.cart.values())

        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price

        total = subtotal + Decimal(newprice)
        return total

    def cart_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item['price'])*item['qty'] for item in self.cart.values())
        total = subtotal + Decimal(deliveryprice)
        return total


    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """ Remove basket from session """
        del self.session[settings.CART_SESSION_ID]
        del self.session['address']
        del self.session['purchase']
        self.save()

    def save(self):
        self.session.modified = True