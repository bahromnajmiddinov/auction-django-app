# Generated by Django 5.0.6 on 2024-06-28 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_summary_alter_auction_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchers',
            name='bid',
            field=models.PositiveIntegerField(default=0),
        ),
    ]