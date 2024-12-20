import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
import authentication
from .models import Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from catalog.models import Product
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/login')
def show_wishlist(request):
    wishlist_items = Product.objects.filter(wishlist__user=request.user)
    context = {
        'user': request.user,
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url='/login')
def delete_wishlist(request, product_id):
    wishlists = Wishlist.objects.filter(user=request.user, product__id=product_id)
    wishlists.delete()
    return redirect('wishlist:show_wishlist')

@login_required(login_url='/login')
@csrf_exempt
def add_wishlist(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
    return redirect('catalog:catalog')

@login_required(login_url='/login')
def show_wishlist_json(request):
    wishlist_items = [
        {
            'id': product.id,
            'nama': product.nama,
            'toko': product.toko,
            'harga': product.harga,
            'gambar': product.gambar if product.gambar else '',
        }
        for product in Product.objects.filter(wishlist__user=request.user)
    ]
    return JsonResponse({'wishlist_items': wishlist_items}, safe=False)

@login_required(login_url='/login')
@csrf_exempt
def delete_wishlist_json(request, product_id):
    wishlists = Wishlist.objects.filter(user=request.user, product__id=product_id)
    if not wishlists.exists():
        return JsonResponse({'status': 'error', 'message': 'Product not found in wishlist'}, status=404)
    wishlists.delete() 
    return JsonResponse({'status': 'success', 'message': 'Product removed from wishlist'})

def add_wishlist_json(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
    if created:
        response = {
            'status': 'success',
            'message': 'Product added to wishlist',
            'product': {
                'id': product.id,
                'nama': product.nama,
                'toko': product.toko,
                'harga': product.harga,
                'gambar': product.gambar if product.gambar else '',
            }
        }
    else:
        response = {
            'status': 'info',
            'message': 'Product is already in your wishlist',
        }
    return JsonResponse(response)

@csrf_exempt
def add_wishlist_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")
            product = get_object_or_404(Product, id=product_id)
            user = request.user
            wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)

            if created:
                response = {
                    'status': 'success',
                    'message': 'Product added to wishlist'
                }
            else:
                response = {
                    'status': 'info',
                    'message': 'Product is already in your wishlist'
                }
            return JsonResponse(response, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


@csrf_exempt
def delete_wishlist_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")
            user = request.user

            wishlists = Wishlist.objects.filter(user=user, product__id=product_id)

            if not wishlists.exists():
                return JsonResponse({'status': 'error', 'message': 'Product not found in wishlist'}, status=404)
            wishlists.delete()
            return JsonResponse({'status': 'success', 'message': 'Product removed from wishlist'}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

@login_required(login_url='/login')
def show_wishlist_flutter(request):
    try:
        wishlist_items = [
            {
                'id': product.id,
                'nama': product.nama,
                'toko': product.toko,
                'harga': product.harga,
                'gambar': product.gambar.url if product.gambar else '',
            }
            for product in Product.objects.filter(wishlist__user=request.user)
        ]

        return JsonResponse({'wishlist_items': wishlist_items}, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
