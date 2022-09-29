from django.contrib import admin

from .models import DeliveryOptions

@admin.register(DeliveryOptions)
class DeliveryOptionsAdmin(admin.ModelAdmin):
    pass

