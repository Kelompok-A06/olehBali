from django.shortcuts import render
from .models import Product

# Create your views here.
def show_catalog(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, "catalog.html", context)