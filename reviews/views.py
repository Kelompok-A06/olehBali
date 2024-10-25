from django.shortcuts import render

# Create your views here.
def show_review(request):
    render(request, "product-review.html")