from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('', show_review, name='review'),
]
