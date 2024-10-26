from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from catalog.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
