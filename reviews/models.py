from django.db import models
from django.conf import settings
from catalog.models import Product
# Create your models here.

class Reviews(models.Model):
    RATINGS_CHOICE = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ratings = models.IntegerField(choices=RATINGS_CHOICE, default=0)
    comments = models.TextField()

