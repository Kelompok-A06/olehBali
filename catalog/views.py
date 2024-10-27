from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from .models import Product

# Create your views here.
def catalog(request):
    category = request.GET.get('kategori', 'all')
    search_query = request.GET.get('search', '')  # Get the search query

    if category == 'makanan_minuman':
        products = Product.objects.filter(kategori='Makanan/Minuman')
    elif category == 'kerajinan_tangan':
        products = Product.objects.filter(kategori='Kerajinan Tangan')
    elif category == 'pakaian':
        products = Product.objects.filter(kategori='Pakaian')
    elif category == 'lain_lain':
        products = Product.objects.filter(kategori='Lain-lain')
    else:
        products = Product.objects.all()   

    if search_query:
        products = products.filter(nama__icontains=search_query)


    paginator = Paginator(products, 14)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'category': category,
        'search_query': search_query
    }
    return render(request, "catalog.html", context)

def show_product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def get_products(request):
    products = Product.objects.all()
    return HttpResponse(serializers.serialize("json", products), content_type="application/json")

def get_products_by_id(request, id):
    product = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", product), content_type="application/json")