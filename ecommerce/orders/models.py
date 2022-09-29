from tabnanny import verbose
from django.db import models

from decimal import Decimal

from django.conf import settings
from django.db import models
from catalogue.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user")
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country_code = models.CharField(max_length=4, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=7, decimal_places=2)
    order_key = models.CharField(max_length=200)
    payment_option = models.CharField(max_length=200, blank=True)
    billing_status = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.created)