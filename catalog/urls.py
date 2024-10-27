from django.conf import settings
from django.urls import path
from catalog.views import catalog, delete_product, add_product
from django.conf.urls.static import static

app_name = 'catalog'

urlpatterns = [
    path('', catalog, name='catalog'),
    path('add_product/', add_product, name='add_product'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)