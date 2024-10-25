from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.IntegerField()
    shop = models.CharField(max_length=255) 
    address = models.CharField(max_length=255)
    description = models.TextField()
