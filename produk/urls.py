from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('json/', get_products, name='get_products'),
    path('json/<int:id>', get_products_by_id, name='get_products_by_id'),
]