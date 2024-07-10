from django.db import models

from auction.models import Auction
from accounts.models import CustomUser, Address


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deleivered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
