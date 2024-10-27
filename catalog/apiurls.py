from django.urls import path
from catalog.views import get_products, get_products_by_id

app_name = 'catalog_api'

urlpatterns = [
    path('', get_products, name='get_products'),
    path('<int:id>', get_products_by_id, name='get_products_by_id'),
]