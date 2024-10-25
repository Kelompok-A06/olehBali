from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('<int:id>', show_review, name='review'),
]
