# Generated by Django 5.1.2 on 2024-10-27 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_product_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='owner',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
