from django import forms
from .models import Product
from django.conf import settings

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nama', 'kategori', 'harga', 'alamat', 'deskripsi', 'gambar', 'gambar_file']  

    def save(self, commit=True, toko=None):
        product = super().save(commit=False)  
        if toko:
            product.toko = toko  
        if commit:
            product.save()
        return product

