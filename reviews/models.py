from django.db import models
from authentication.models import User

# Create your models here.


class TempProduct(models.Model):
    pass

class Reviews(models.Model):
    RATINGS_CHOICE = (0,1,2,3,4,5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(TempProduct, on_delete=models.CASCADE)
    ratings = models.IntegerField(choices=RATINGS_CHOICE, default=0)
    comments = models.TextChoices()

