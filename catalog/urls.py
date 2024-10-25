from django.urls import path
from catalog.views import *

app_name = 'catalog'

urlpatterns = [
    path('', get_products, name='get_products'),
    path('<int:id>', get_products_by_id, name='get_products_by_id'),
]