from django.shortcuts import render
from catalog.models import Product
from .models import Reviews
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from authentication.models import User
from django.core import serializers

# Create your views here.
def show_review(request, id):
    product = Product.objects.get(pk=id)
    context = {
        'product' : product,
        'user' : request.user,
        'reviews' : Reviews.objects.filter(product=product)
    }
    return render(request, "product-review.html", context)

def review_json(request, id):
    product = Product.objects.get(pk=id)
    reviews = Reviews.objects.filter(product=product)
    review_data = [
        {
            'id': review.pk,  
            'ratings': review.ratings,
            'comments': review.comments,
            'username': review.user.username, 
        }
        for review in reviews
    ]
    
    return JsonResponse(review_data, safe=False) 

@csrf_exempt
@require_POST
def add_review(request, id):
    ratings = request.POST.get("ratings")
    comments = strip_tags(request.POST.get("comments"))
    product = Product.objects.get(pk=id)
    user = request.user;

    new_review = Reviews(
        ratings=ratings, comments=comments,
        user=user,product=product,
    )
    new_review.save()

    return HttpResponse(b"CREATED", status=201)