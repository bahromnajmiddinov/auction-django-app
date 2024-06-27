from django.db import models

from accounts.models import CustomUser
from auctions.models import Auction


class Card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cards')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{ self.user.email }\'s card | { self.id }'


class CardItem(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='items')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='user_cart_items')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{ self.card.id } | { self.id }'
