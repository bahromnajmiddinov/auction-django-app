from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Auction
from .utils import time_scheduler


@receiver(post_save, sender=Auction)
def model_saved(sender, instance, created, **kwargs):
    if created:
        if instance.start_time:
            time_scheduler(instance.start_time, f'auction_start_time_{instance.id}', instance.id, task='start_time')
        if instance.end_time:
            time_scheduler(instance.end_time, f'auction_end_time_{instance.id}', instance.id, task='end_time')


@receiver(pre_save, sender=Auction)
def model_updated(sender, instance, **kwargs):
    if instance.start_time:
        time_scheduler(instance.start_time, f'auction_start_time_{instance.id}', instance.id, task='start_time')
    if instance.end_time:
        time_scheduler(instance.end_time, f'auction_end_time_{instance.id}', instance.id, task='end_time')

