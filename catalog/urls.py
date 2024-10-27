from django.urls import path
from catalog.views import catalog, delete_product

app_name = 'catalog'

urlpatterns = [
    path('', catalog, name='catalog'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
]