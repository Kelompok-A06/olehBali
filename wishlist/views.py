import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
import authentication
from .models import Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from catalog.models import Product
from .forms import AddWishlistStatusForm

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
def update_status(request, product_id):
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product__id=product_id)

    if request.method == 'POST':
        form = AddWishlistStatusForm(request.POST, instance=wishlist_item)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    else:
        form = AddWishlistStatusForm(instance=wishlist_item)

    return render(request, 'update_status.html', {'form': form, 'wishlist_item': wishlist_item})

# def add_status(request):
#     if request.method == 'POST':
#         form = AddWishlistStatusForm(request.POST)
#         if form.is_valid():
#             product_id = request.POST.get('product_id')
#             product = get_object_or_404(Product, id=product_id)
#             product_status = form.cleaned_data['product_status']
#             Wishlist.objects.create(user=request.user, product=product, product_status=product_status)
#         return redirect('wishlist:show_wishlist')
#     form = AddWishlistStatusForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'add_status.html', context)

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