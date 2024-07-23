from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask, CrontabSchedule

from .models import Auction
from .utils import time_scheduler


def update_task_or_not(periodic_task, data_obj):
    add_new_task = True
    if periodic_task.exists():
        crontab = periodic_task.crontab
        if (crontab.minute != data_obj.minute or crontab.hour != data_obj.hour or
        crontab.day_of_month != data_obj.day or crontab.month_of_year != data_obj.month):
            pass
        else:
            add_new_task = False 
    
    return add_new_task


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
        periodic_taks_name = f'auction_start_time_{instance.id}'
        
        periodic_task = PeriodicTask.objects.filter(name=periodic_taks_name)
        
        add_new_task = update_task_or_not(periodic_task, instance.start_time)
        
        if add_new_task:
            time_scheduler(instance.start_time, periodic_taks_name, instance.id, task='start_time')
            
    if instance.end_time:
        periodic_taks_name = f'auction_end_time_{instance.id}'
        
        periodic_task = PeriodicTask.objects.filter(name=periodic_taks_name)
        
        add_new_task = update_task_or_not(periodic_task, instance.end_time)
        
        if add_new_task:
            time_scheduler(instance.end_time, f'auction_end_time_{instance.id}', instance.id, task='end_time')

