from django.urls import path
from catalog.views import catalog, show_product_detail

app_name = 'catalog'

urlpatterns = [
    path('', catalog, name='catalog'),
    path('<int:id>', show_product_detail, name='show_product_detail')
]