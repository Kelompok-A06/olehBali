from django.urls import path
from .views import *
from catalog.views import get_products_by_id

app_name = 'reviews'

urlpatterns = [
    path('<int:id>', show_review, name='review'),
    path('add-review/<int:id>', add_review, name='add_review'),
    path('api/', review_json_all, name='review_json_all'),
    path('api-product/<int:id>', get_products_by_id, name='get_product_by_id'),
    path('api-flutter/', review_json_all_flutter, name='review_json_all_flutter'),
    path('api/<int:id>', review_json, name='review_json'),
    path('api/get/<int:id>', chosen_review_json, name='chosen_review_json'),
    path('delete/<int:id>', delete_review_json, name='delete_review'),
    path('delete-flutter/', delete_review_flutter, name='delete_review'),
    path('add-review-flutter/', create_review_flutter, name="add_review_flutter" )
]
