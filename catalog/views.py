import json
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm 

# Create your views here.
@login_required
def catalog(request):
    category = request.GET.get('kategori', 'all')
    search_query = request.GET.get('search', '')  
    current_user = request.user
    
    if current_user.role == 'owner':
        products = Product.objects.filter(toko=request.user.username)
        if category == 'makanan_minuman':
            products = Product.objects.filter(toko=request.user.username, kategori='Makanan/Minuman')
        elif category == 'kerajinan_tangan':
            products = Product.objects.filter(toko=request.user.username, kategori='Kerajinan Tangan')
        elif category == 'pakaian':
            products = Product.objects.filter(toko=request.user.username, kategori='Pakaian')
        elif category == 'lain_lain':
            products = Product.objects.filter(toko=request.user.username, kategori='Lain-lain')
    
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
        'search_query': search_query,
        'current_user': current_user
    }
    return render(request, "catalog.html", context)

@login_required
def get_products(request, category=None):
    current_user = request.user
    search_query = request.GET.get('search', '')

    if current_user.role == 'owner':
        products = Product.objects.filter(toko=request.user.username)
        if category == 'makanan_minuman':
            products = products.filter(kategori='Makanan/Minuman')
        elif category == 'kerajinan_tangan':
            products = products.filter(kategori='Kerajinan Tangan')
        elif category == 'pakaian':
            products = products.filter(kategori='Pakaian')
        elif category == 'lain_lain':
            products = products.filter(kategori='Lain-lain')
    else:
        products = Product.objects.all()
        if category == 'makanan_minuman':
            products = products.filter(kategori='Makanan/Minuman')
        elif category == 'kerajinan_tangan':
            products = products.filter(kategori='Kerajinan Tangan')
        elif category == 'pakaian':
            products = products.filter(kategori='Pakaian')
        elif category == 'lain_lain':
            products = products.filter(kategori='Lain-lain')

    if search_query:
        products = products.filter(nama__icontains=search_query)

    return HttpResponse(serializers.serialize("json", products), content_type="application/json")

@login_required
def get_products_by_id(request, id):
    product = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", product), content_type="application/json")

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('/catalog/')  

@login_required
@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True, toko=request.user.username) 
            return redirect('/catalog/')  
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})

@login_required
@csrf_exempt
def api_add_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_product = Product.objects.create(
            nama=data["nama"],
            kategori=data["kategori"],
            harga=int(data["harga"]),
            toko=data["toko"],
            alamat=data["alamat"],
            deskripsi=data["deskripsi"],
            gambar="",
            gambar_file=data["gambar_file"]
        )
        new_product.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@login_required
@csrf_exempt
def api_delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            product = get_object_or_404(Product, id=product_id)
            if request.user.role == 'owner' and product.toko == request.user.username:
                product.delete()
                return JsonResponse({'message': 'Product deleted successfully'})
            else:
                return JsonResponse({'error': 'Permission denied'}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def get_current_user(request):
    user = request.user
    user_data = {
        'username': user.username,
        'role': user.role,
    }
    return JsonResponse(user_data)