from django.db import models

class Product(models.Model):
    JENIS_KATEGORI = [
        ('kerajinan_tangan', 'Kerajinan Tangan'),
        ('makanan_minuman', 'Makanan/Minuman'),
        ('pakaian', 'Pakaian'),
        ('lain_lain', 'Lain-lain'),
    ]
    nama = models.CharField(max_length=255)
    kategori = models.CharField(max_length=50, choices=JENIS_KATEGORI, default='lain-lain')
    harga = models.IntegerField()
    toko = models.CharField(max_length=255)
    alamat = models.CharField(max_length=255)
    deskripsi = models.TextField()
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True, blank=True)


