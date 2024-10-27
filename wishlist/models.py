from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from catalog.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    PRODUCT_STATUS =[
        (1, 'Should Buy'),
        (2, 'Interested'),
        (3, 'Maybe Later'),
    ]
    product_status = models.IntegerField(choices=PRODUCT_STATUS, default=3)  

    def __str__(self):
        return f"{self.user.username}'s Wishlist status for {self.product.name}"