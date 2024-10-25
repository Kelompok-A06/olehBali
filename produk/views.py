from .models import Product
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

def get_products(request):
    products = Product.objects.all()
    return HttpResponse(serializers.serialize("json", products), content_type="application/json")

def get_products_by_id(request, id):
    try:
        product = Product.objects.filter(pk=id)
        return HttpResponse(serializers.serialize("json", product), content_type="application/json")
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

