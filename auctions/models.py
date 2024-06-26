# TODO: unique links for auctions that user can create and schedule
# TODO: link requests, that auction owner can accept for private and OC type of auctions
# TODO: Add Tag model
# TODO: Add summary for auctions
# TODO: Add alt for images and videos
# TODO: Add date time fields to additional fields

from django.db import models
from django.urls import reverse

import uuid
from django_ckeditor_5.fields import CKEditor5Field

from accounts.models import CustomUser
from .validators import validate_video_file_extension


AUCTION_TYPE_CHOICES = (
    ('PB' , 'Public'),        # all users can see the auction
    ('PR' , 'Private'),       # only invited users can see the auction 
    ('OC', 'Only Contacts'),  # invited and owner's contacts can see the auction
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='auctions')
    main_image = models.ImageField(upload_to=auction_image_path)
    type = models.CharField(max_length=2, choices=AUCTION_TYPE_CHOICES, default='PB')
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = CKEditor5Field('Text', config_name='default')
    starter_price = models.PositiveIntegerField(default=0)
    auction_price = models.PositiveIntegerField(default=0)
    participants = models.ManyToManyField(CustomUser, through='ParticipantData', related_name='participanted_auctions')
    user_watchers = models.ManyToManyField(CustomUser, through='Watchers', related_name='watched_auctions')
    user_like = models.ManyToManyField(CustomUser, through='Like', related_name='liked_auctions')
    
    active = models.BooleanField(default=False)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    permissions = models.ManyToManyField(CustomUser, through='AuctionUserPermission')
    
    class Meta:
        ordering = ['-created', '-updated']
    
    def __str__(self):
        return self.title
    
    @property
    def get_absolute_url(self):
        return reverse('auction', args=[self.slug])
    
    @property
    def get_current_price(self):
        return self.starter_price if self.starter_price > self.auction_price else self.auction_price
    
    @property
    def get_main_image(self):
        return self.main_image.url
    

class ParticipantData(models.Model):
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Watchers(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid = models.PositiveIntegerField()


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class AuctionUserPermission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_add_admin = models.BooleanField(default=False)


class ImageField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=auction_additional_image_path)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='image_fields')


class VideoField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.FileField(upload_to=auction_additional_video_path, validators=[validate_video_file_extension])
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='video_fields')


class AdditionalField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='additional_fields')
    icon = models.ImageField(upload_to=additional_field_icon_path)
    title = models.CharField(max_length=30)
    description = CKEditor5Field('Text', config_name='default')


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='auction_comments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
