from django.db import models

from auctions.models import Auction
from accounts.models import CustomUser, Address


ORDER_PAYMENT_CHOICES = (
    ('ST', 'STRIPE'),
)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deleivered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=2, choices=ORDER_PAYMENT_CHOICES)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
