from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import shortuuid


class Link(models.Model):
    path = models.CharField(_('Path'), max_length=24, default=shortuuid.uuid, editable=False, unique=True)
    limit_by_time = models.DateTimeField(_('Limit By Time'), blank=True, null=True)
    limit_by_clicks = models.PositiveIntegerField(_('Limit By Clicks'), blank=True, null=True)
    users = models.ManyToManyField('accounts.CustomUser', verbose_name=_('Users'))
    auction = models.ForeignKey('auctions.Auction', on_delete=models.CASCADE, verbose_name=_('Auction'))
    clicks = models.PositiveIntegerField(_('Clicks'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    
    def __str__(self):
        return f'Link {self.path} for auction {self.auction.id}'
    
    def is_expired(self):
        if self.limit_by_clicks >= self.users.count() or self.limit_by_time >= timezone.now():
            return True
        return False
    
