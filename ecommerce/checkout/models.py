from django.db import models

from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryOptions(models.Model):
    """ The table contains all valid shipping methods """

    DELIVERY_CHOICES = [
        ('IS', 'В магазин'),
        ('INP', 'В отделение Новой Почты'),
        ('CD', 'Доставка курьером')
    ]

    delivery_name = models.CharField(verbose_name=_(
        'название доставки'), help_text=_('обязательное поле'), max_length=255)
    delivery_price = models.DecimalField(verbose_name=_('стоимость доставки'), help_text=_('Максимум 99999.99'),
                                         error_messages={'name': {'max_length': _(
                                             'Стоимость должна быть в пределах от 0 до 9999.99')}},
                                         max_digits=7, decimal_places=2)
    delivery_method = models.CharField(choices=DELIVERY_CHOICES, verbose_name=_(
        'вариант доставки'), help_text=_('обязательно'), max_length=255)
    delivery_timeframe = models.CharField(verbose_name=_(
        'сроки доставки'), help_text=_('обязательно'), max_length=255)
    delivery_window = models.CharField(verbose_name=_(
        'временное окно доставки'), help_text=_('обязательно'), max_length=255)
    order = models.IntegerField(verbose_name=_('Список заказа'), help_text=_('обязательно'), default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Опция доставки')
        verbose_name_plural = _('Опции доставок')

    def __str__(self) -> str:
        return self.delivery_name


class PaymentSelection(models.Model):
    """ payment options """

    name = models.CharField(verbose_name=_('название'), help_text=_('обязательно'), max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Вариант оплаты')
        verbose_name_plural = _('Варианты платежей')

    def __str__(self):
        return self.name

