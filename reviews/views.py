from django.shortcuts import render
from catalog.models import Product
from .models import Reviews

# Create your views here.
def show_review(request, id):
    product = Product.objects.get(pk=id)
    context = {
        'product' : product
    }
    return render(request, "product-review.html", context)