from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('deliverychoices/', views.deliverychoices, name='deliverychoices'),
    path('cart_update_delivery/', views.cart_update_delivery, name='cart_update_delivery'),
    path('delivery_address/', views.delivery_address, name='delivery_address'),
    path('payment_selection/', views.payment_selection, name='payment_selection'),
    path('payment_successful/', views.payment_successful, name='payment_successful'),
]