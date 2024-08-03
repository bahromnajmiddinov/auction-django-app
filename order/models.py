from django.db import models
from django.utils.translation import gettext_lazy as _

from auctions.models import Auction
from accounts.models import CustomUser, Address


ORDER_PAYMENT_CHOICES = (
    ('ST', 'STRIPE'),
)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, verbose_name=_('User'))
    address = models.ForeignKey(Address, on_delete=models.PROTECT, verbose_name=_('Address'))
    total_amount = models.DecimalField(_('Total Amount'), max_digits=10, decimal_places=2)
    delivered = models.BooleanField(_('Delivered'), default=False)
    paid = models.BooleanField(_('Paid'), default=False)
    payment_method = models.CharField(_('Payment Method'), max_length=2, choices=ORDER_PAYMENT_CHOICES)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
