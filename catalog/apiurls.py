from django.urls import path
from catalog.views import get_products, get_products_by_id, get_current_user, api_delete_product, api_add_product

app_name = 'catalog_api'

urlpatterns = [
    path('', get_products, name='get_products'),
    path('category/<str:category>/', get_products, name='get_products_by_category'),
    path('<int:id>', get_products_by_id, name='get_products_by_id'),
    path('user/', get_current_user, name='get_current_user'),
    path('add_product/', api_add_product, name='api_add_product'), 
    path('delete_product/<int:product_id>/', api_delete_product, name='api_delete_product'),
]