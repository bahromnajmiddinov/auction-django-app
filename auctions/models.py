# TODO: link requests, that auction owner can accept for private and OC type of auctions

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import uuid
from django_ckeditor_5.fields import CKEditor5Field

from labeler.models import Category, Tag
from accounts.models import CustomUser
from .validators import validate_video_file_extension


AUCTION_TYPE_CHOICES = (
    ('PB' , _('Public')),        # all users can see the auction
    ('PR' , _('Private')),       # only invited users can see the auction 
    ('OC', _('Only Contacts')),  # invited and owner's contacts can see the auction
)


def auction_image_path (instance, filename):
    ext = filename.split('.')[-1]
    path = f'media/auctions/{instance.id}/images/main_image.{ext}'
    return path


def auction_additional_image_path(instance, filename):
    ext = filename.split('.')[-1]
    path = f'media/auctions/{instance.id}/images/additional_image.{ext}'
    return path


def auction_additional_video_path(instance, filename):
    ext = filename.split('.')[-1]
    path = f'media/auctions/{instance.id}/videos/additional_video.{ext}'
    return path


def additional_field_icon_path(instance, filename):
    ext = filename.split('.')[-1]
    path = f'media/auctions/additional_fields/{instance.id}/icons/icon.{ext}'
    return path


class Auction(models.Model):
    id = models.UUIDField(_('Id'), primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='auctions', verbose_name=_('Owner'))
    winner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='winner', verbose_name=_('Winner'))
    main_image = models.ImageField(_('Main Image'), upload_to=auction_image_path)
    type = models.CharField(_('Type'), max_length=2, choices=AUCTION_TYPE_CHOICES, default='PB')
    title = models.CharField(_('Title'), max_length=60)
    slug = models.SlugField(_('Slug'), )
    summary = models.CharField(_('Summary'), max_length=200)
    description = CKEditor5Field(_('Description'), config_name='default')
    starter_price = models.PositiveIntegerField(_('Starter Price'), default=0)
    auction_price = models.PositiveIntegerField(_('Auction Price'), default=0)
    participants = models.ManyToManyField(CustomUser, through='ParticipantData', related_name='participanted_auctions', verbose_name=_('Participants'))
    user_watchers = models.ManyToManyField(CustomUser, through='Watchers', related_name='watched_auctions', verbose_name=_('User Watchers'))
    user_likes = models.ManyToManyField(CustomUser, through='Like', related_name='liked_auctions', verbose_name=_('User Likes'))
    
    active = models.BooleanField(_('Active'), default=False)
    start_time = models.DateTimeField(_('Start Time'), blank=True, null=True)
    end_time = models.DateTimeField(_('End Time'), )
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    
    categories = models.ManyToManyField(Category, related_name='auction_categories', verbose_name=_('Categories'))
    tags = models.ManyToManyField(Tag, related_name='auction_tags', verbose_name=_('Tags'))
    
    permissions = models.ManyToManyField(CustomUser, through='AuctionUserPermission', verbose_name='Permissions')
    
    class Meta:
        ordering = ['-created', '-updated']
    
    def __str__(self):
        return self.title
    
    @property
    def get_absolute_url(self):
        if self.type == 'PB':
            return reverse('auction', args=[self.slug])
        return reverse('auction-private', args=[self.slug])
    
    @property
    def get_current_price(self):
        return self.starter_price if self.starter_price > self.auction_price else self.auction_price
    
    @property
    def get_main_image(self):
        return self.main_image.url
    
    @property
    def get_start_time(self):
        now = timezone.now()
        if self.start_time is None or self.start_time >= now:
            return True
        elif self.start_time < now:
            return False
    
    @property
    def get_end_time(self):
        now = timezone.now()
        if self.end_time is None or self.end_time >= now:
            return True
        elif self.end_time < now:
            return False
    
    @property
    def get_time_now(self):
        return timezone.now()
    

class ParticipantData(models.Model):
    '''
    Auction participants Through Table
    '''
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField(default=0)


class Watchers(models.Model):
    '''
    Auction user_watchers Through Table
    '''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    '''
    Auction user_likes Through Table
    '''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class AuctionUserPermission(models.Model):
    '''
    Auction User Permissions Through Table
    '''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_add_admin = models.BooleanField(default=False)


class ImageField(models.Model):
    '''
    Auction Additional Image Field
    '''
    id = models.UUIDField(_('Id'), primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(_('Image'), upload_to=auction_additional_image_path)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='image_fields', verbose_name=_('Auction'))
    
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)


class VideoField(models.Model):
    '''
    Auction Video Field
    '''
    id = models.UUIDField(_('Id'), primary_key=True, default=uuid.uuid4, editable=False)
    video = models.FileField(_('Video'), upload_to=auction_additional_video_path, validators=[validate_video_file_extension])
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='video_fields', verbose_name=_('Auction'))
    
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)


class AdditionalField(models.Model):
    '''
    Auction Additional Field
    '''
    id = models.UUIDField(_('Id'), primary_key=True, default=uuid.uuid4, editable=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='additional_fields', verbose_name=_('Auction'))
    icon = models.ImageField(_('Icon'), upload_to=additional_field_icon_path)
    title = models.CharField(_('Title'), max_length=30)
    description = CKEditor5Field(_('Description'), config_name='default')
    
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('UPdated'), auto_now=True)


class Message(models.Model):
    '''
    Auction Message model
    '''
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='messages')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=250)
    
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    '''
    Auction Comment Model
    '''
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='auction_comments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.text} {self.auction}'


class LocationData(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='users_locations')
    country = models.CharField(max_length=56)
    city = models.CharField(max_length=85)
    ip_address = models.CharField(max_length=30)
