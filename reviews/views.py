import json
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
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def show_review(request, id):
    product = Product.objects.get(pk=id)
    context = {
        'product' : product,
        'user' : request.user,
        'reviews' : Reviews.objects.filter(product=product)
    }
    return render(request, "product-review.html", context)

@login_required(login_url='/login')
def review_json_all(request):
    reviews = Reviews.objects.all()
    return HttpResponse(serializers.serialize("json", reviews), content_type="application/json")

@login_required(login_url='/login')
def review_json_all_flutter(request):
    reviews = Reviews.objects.all()
    review_data = [
        {
            'model' : 'reviews.reviews',
            'pk' : review.pk,
            'fields' : {
                'user' : review.user.pk, 
                'ratings': review.ratings,
                'comments': review.comments,
                'username': review.user.username, 
                'productName' : review.product.nama,
            }
        }
        for review in reviews
    ]
    return JsonResponse(review_data, safe=False)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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


@csrf_exempt
def create_review_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = int(data["id"])
        user=request.user 
        product=Product.objects.get(pk=id)
        ratings=int(data["ratings"])
        comments=data["comments"]
        review_id = data["review_id"]
        if not review_id:
            new_review = Reviews.objects.create(
                user=user, 
                product=product,
                ratings=ratings,
                comments=comments,
            )
            new_review.save()
            return JsonResponse({"status": "success"}, status=201)
        else:
            review_id = int(review_id)
            review = Reviews.objects.get(pk=review_id, user=user, product=product)
            review.ratings = ratings
            review.comments = comments
            review.save()
            return JsonResponse({"status": "updated"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@login_required(login_url='/login')
@csrf_exempt
def delete_review_json(request, id):
    review = Reviews.objects.get(pk=id)
    review.delete() 
    return JsonResponse({'status': 'DELETED', 'message': 'Review Deleted'})
