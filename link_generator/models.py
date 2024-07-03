from django.db import models
from django.utils import timezone

import shortuuid


class Link(models.Model):
    path = models.CharField(max_length=24, default=shortuuid.uuid, editable=False, unique=True)
    limit_by_time = models.DateTimeField(blank=True, null=True)
    limit_by_clicks = models.PositiveIntegerField(blank=True, null=True)
    users = models.ManyToManyField('accounts.CustomUser')
    auction = models.ForeignKey('auctions.Auction', on_delete=models.CASCADE)
    clicks = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Link {self.path} for auction {self.auction.id}'
    
    def is_expired(self):
        if self.limit_by_users >= self.users.count() or self.limit_by_time >= timezone.now():
            return True
        return False
    
