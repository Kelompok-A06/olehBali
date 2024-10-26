from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
import authentication
from .models import Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from catalog.models import Product

@login_required(login_url='/login')
def show_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items' : wishlist_items,
    }
    return render(request, "wishlist.html", context)

@login_required(login_url='/login')
def delete_wishlist(request, id):
    wishlist_item = get_object_or_404(Wishlist, pk=id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist:show_wishlist')

