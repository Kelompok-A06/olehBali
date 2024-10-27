from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
@login_required(login_url='/login')
def catalog(request):
    category = request.GET.get('kategori', 'all')
    search_query = request.GET.get('search', '')  
    current_user = request.user
    
    if current_user.role == 'owner':
        products = Product.objects.filter(owner=request.user)
        if category == 'makanan_minuman':
            products = Product.objects.filter(owner=request.user, kategori='Makanan/Minuman')
        elif category == 'kerajinan_tangan':
            products = Product.objects.filter(owner=request.user, kategori='Kerajinan Tangan')
        elif category == 'pakaian':
            products = Product.objects.filter(owner=request.user, kategori='Pakaian')
        elif category == 'lain_lain':
            products = Product.objects.filter(owner=request.user, kategori='Lain-lain')
    
    else:
        products = Product.objects.all()
        if category == 'makanan_minuman':
            products = Product.objects.filter(kategori='Makanan/Minuman')
        elif category == 'kerajinan_tangan':
            products = Product.objects.filter(kategori='Kerajinan Tangan')
        elif category == 'pakaian':
            products = Product.objects.filter(kategori='Pakaian')
        elif category == 'lain_lain':
            products = Product.objects.filter(kategori='Lain-lain')

    

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

@login_required(login_url='/login')
def get_products(request):
    products = Product.objects.all()
    return HttpResponse(serializers.serialize("json", products), content_type="application/json")

@login_required(login_url='/login')
def get_products_by_id(request, id):
    product = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", product), content_type="application/json")

@login_required
@csrf_exempt
def delete_product(request, product_id):
    if request.method == "POST" and request.user.role == 'owner':
        product = get_object_or_404(Product, id=product_id, owner=request.user)
        product.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)