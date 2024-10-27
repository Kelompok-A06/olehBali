from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['nama', 'toko', 'harga', 'kategori']

admin.site.register(Product, ProductAdmin)