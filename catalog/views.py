from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Product

# Create your views here.
def show_catalog(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, "catalog.html", context)

def get_products(request):
    products = Product.objects.all()
    return HttpResponse(serializers.serialize("json", products), content_type="application/json")

def get_products_by_id(request, id):
    product = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", product), content_type="application/json")