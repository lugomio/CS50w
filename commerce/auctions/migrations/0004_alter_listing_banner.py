# Generated by Django 5.0.6 on 2024-05-20 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='banners'),
        ),
    ]