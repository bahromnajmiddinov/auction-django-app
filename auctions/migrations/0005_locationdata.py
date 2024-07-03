# Generated by Django 5.0.6 on 2024-07-01 04:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_user_like_auction_user_likes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=56)),
                ('city', models.CharField(max_length=85)),
                ('ip_address', models.CharField(max_length=30)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_locations', to='auctions.auction')),
            ],
        ),
    ]