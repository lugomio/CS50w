# Generated by Django 5.0.6 on 2024-05-21 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_changed_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='changed_at',
        ),
    ]
