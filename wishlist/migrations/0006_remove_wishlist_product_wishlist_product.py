# Generated by Django 5.1.2 on 2024-10-27 11:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20241025_1419'),
        ('wishlist', '0005_remove_wishlist_product_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='catalog.product'),
            preserve_default=False,
        ),
    ]
