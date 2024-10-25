from .models import Product
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

def get_products(request):
    products = Product.objects.all()
    return HttpResponse(serializers.serialize("json", products), content_type="application/json")

def get_products_by_id(request, id):
    product = Product.objects.get(pk=id)
    return HttpResponse(serializers.serialize("json", product), content_type="application/json")
