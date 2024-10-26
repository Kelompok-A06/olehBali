from django.urls import path
from .views import *

app_name = 'reviews'

urlpatterns = [
    path('<int:id>', show_review, name='review'),
    path('add-review/<int:id>', add_review, name='add_review'),
    path('api/<int:id>', review_json, name='review_json'),
    path('api/get/<int:id>', chosen_review_json, name='chosen_review_json'),
    path('delete/<int:id>', delete_review, name='delete_review'),
]
