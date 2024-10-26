from django.shortcuts import render, redirect
from catalog.models import Product
from .models import Reviews
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from authentication.models import User
from django.core import serializers
from django.urls import reverse

# Create your views here.
def show_review(request, id):
    product = Product.objects.get(pk=id)
    context = {
        'product' : product,
        'user' : request.user,
        'reviews' : Reviews.objects.filter(product=product)
    }
    return render(request, "product-review.html", context)

def review_json_all(request):
    reviews = Reviews.objects.all()
    return HttpResponse(serializers.serialize("json", reviews), content_type="application/json")

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

def chosen_review_json(request, id):
    review = Reviews.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", review), content_type="application/json")

@csrf_exempt
@require_POST
def add_review(request, id):
    ratings = request.POST.get("ratings")
    comments = strip_tags(request.POST.get("comments"))
    review_id = request.POST.get("review_id")
    product = Product.objects.get(pk=id)
    user = request.user;

    if not comments:
        return JsonResponse({
            'status': 'ERROR',
            'errors': {
                'name': 'Comments cannot be blank.',
            }
        }, status=400)

    if not review_id:
        new_review = Reviews(
            ratings=ratings, comments=comments,
            user=user,product=product,
        )
        new_review.save()

        return JsonResponse({'status': 'CREATED',}, status=201)
    else:
        review = Reviews.objects.get(pk=review_id, user=user, product=product)
        review.ratings = ratings
        review.comments = comments
        review.save()
        return JsonResponse({'status': 'UPDATED'}, status=200)


def delete_review(request, id):
    review = Reviews.objects.get(pk=id)
    product = review.product
    review.delete()
    return redirect(reverse('reviews:review', kwargs={'id': product.id}))

