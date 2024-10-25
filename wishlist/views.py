from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import authentication
from .models import Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from django.urls import reverse

@login_required(login_url='/login')
def show_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'name': request.user,
        'wishlist_items' : wishlist_items
    }
    return render(request, "wishlist.html", context)

@login_required(login_url='/login')
def delete_wishlist(request, id):
    wishlist = Wishlist.objects.get(pk=id, user=request.user)
    wishlist.delete()
    return redirect('show_wishlist')

# fungsi delete ajax

