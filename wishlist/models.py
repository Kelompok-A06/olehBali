from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# import katalog

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tanggal = models.DateField(auto_now_add=True)