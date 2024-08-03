# Generated by Django 5.0.6 on 2024-08-02 16:07

import auctions.models
import auctions.validators
import django.db.models.deletion
import django_ckeditor_5.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auction_winner_alter_auction_end_time'),
        ('labeler', '0002_alter_category_name_alter_category_slug_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalfield',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_fields', to='auctions.auction', verbose_name='Auction'),
        ),
        migrations.AlterField(
            model_name='additionalfield',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='additionalfield',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='additionalfield',
            name='icon',
            field=models.ImageField(upload_to=auctions.models.additional_field_icon_path, verbose_name='Icon'),
        ),
        migrations.AlterField(
            model_name='additionalfield',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='additionalfield',
            name='title',
            field=models.CharField(max_length=30, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='additionalfield',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='UPdated'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='auction_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Auction Price'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='categories',
            field=models.ManyToManyField(related_name='auction_categories', to='labeler.category', verbose_name='Categories'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='end_time',
            field=models.DateTimeField(verbose_name='End Time'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='main_image',
            field=models.ImageField(upload_to=auctions.models.auction_image_path, verbose_name='Main Image'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='participants',
            field=models.ManyToManyField(related_name='participanted_auctions', through='auctions.ParticipantData', to=settings.AUTH_USER_MODEL, verbose_name='Participants'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='permissions',
            field=models.ManyToManyField(through='auctions.AuctionUserPermission', to=settings.AUTH_USER_MODEL, verbose_name='Permissions'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='slug',
            field=models.SlugField(verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start Time'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='starter_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Starter Price'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='summary',
            field=models.CharField(max_length=200, verbose_name='Summary'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='tags',
            field=models.ManyToManyField(related_name='auction_tags', to='labeler.tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='title',
            field=models.CharField(max_length=60, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='type',
            field=models.CharField(choices=[('PB', 'Public'), ('PR', 'Private'), ('OC', 'Only Contacts')], default='PB', max_length=2, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='user_likes',
            field=models.ManyToManyField(related_name='liked_auctions', through='auctions.Like', to=settings.AUTH_USER_MODEL, verbose_name='User Likes'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='user_watchers',
            field=models.ManyToManyField(related_name='watched_auctions', through='auctions.Watchers', to=settings.AUTH_USER_MODEL, verbose_name='User Watchers'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winner', to=settings.AUTH_USER_MODEL, verbose_name='Winner'),
        ),
        migrations.AlterField(
            model_name='imagefield',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_fields', to='auctions.auction', verbose_name='Auction'),
        ),
        migrations.AlterField(
            model_name='imagefield',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='imagefield',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='imagefield',
            name='image',
            field=models.ImageField(upload_to=auctions.models.auction_additional_image_path, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='imagefield',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
        migrations.AlterField(
            model_name='videofield',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_fields', to='auctions.auction', verbose_name='Auction'),
        ),
        migrations.AlterField(
            model_name='videofield',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='videofield',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='videofield',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated'),
        ),
        migrations.AlterField(
            model_name='videofield',
            name='video',
            field=models.FileField(upload_to=auctions.models.auction_additional_video_path, validators=[auctions.validators.validate_video_file_extension], verbose_name='Video'),
        ),
    ]