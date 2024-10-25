from django.shortcuts import render
from catalog.models import Product
from .models import Reviews
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

# Create your views here.
def show_review(request, id):
    product = Product.objects.get(pk=id)
    context = {
        'product' : product
    }
    return render(request, "product-review.html", context)

@csrf_exempt
@require_POST
def add_review(request, id):
    ratings = request.POST.get("price")
    comments = strip_tags(request.POST.get("comments"))
    product = Product.objects.get(pk=id)
    user = request.user;

    new_review = Reviews(
        ratings=ratings, comments=comments,
        user=user,product=product,
    )
    new_review.save()

    return JsonResponse({
        'status': 'CREATED',
        'ratings': ratings,
        'comments': comments
    }, status=201)