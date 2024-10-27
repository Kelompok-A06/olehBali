from django.conf import settings
from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_TYPES = [
        ('kerajinan_tangan', 'Kerajinan Tangan'),
        ('makanan_minuman', 'Makanan/Minuman'),
        ('pakaian', 'Pakaian'),
        ('lain_lain', 'Lain-lain'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=50, choices=CATEGORY_TYPES)
    harga = models.IntegerField()
    toko = models.CharField(max_length=255) 
    alamat = models.CharField(max_length=255)
    deskripsi = models.TextField()
    gambar = models.CharField(max_length=255, null=True, blank=True)
    gambar_file = models.ImageField(upload_to='images/', null=True, blank=True)

# class OwnerProduct(models.Model):
#     CATEGORY_TYPES = [
#         ('kerajinan_tangan', 'Kerajinan Tangan'),
#         ('makanan_minuman', 'Makanan/Minuman'),
#         ('pakaian', 'Pakaian'),
#         ('lain_lain', 'Lain-lain'),
#     ]
    
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     nama = models.CharField(max_length=255)
#     kategori = models.CharField(max_length=50, choices=CATEGORY_TYPES)
#     harga = models.IntegerField()
#     toko = models.CharField(max_length=255) 
#     alamat = models.CharField(max_length=255)
#     deskripsi = models.TextField()
#     gambar = models.CharField(max_length=255, null=True, blank=True)
#     gambar_file = models.ImageField(upload_to='images/', null=True, blank=True)
    