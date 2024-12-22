from django.urls import path
from authentication.views import *
from wishlist.views import *
from . import views

app_name = 'wishlist'
urlpatterns =[
    path('', show_wishlist, name='show_wishlist'),
    path('delete_wishlist/<int:product_id>/', delete_wishlist, name='delete_wishlist'),
    path('json/show_wishlist/', show_wishlist_json, name='show_wishlist_json'),
    path('json/delete_wishlist/<int:product_id>/', delete_wishlist_json, name='delete_wishlist_json'),
    path('add_wishlist/<int:product_id>/', add_wishlist, name='add_wishlist'),
    path('json/add_wishlist/<int:product_id>/', add_wishlist_json, name='add_wishlist_json'),
    path('json/show_wishlist_flutter', views.show_wishlist_flutter, name='show_wishlist_flutter'),
    path('json/add_wishlist_flutter', views.add_wishlist_flutter, name='add_wishlist_flutter'),
    path('json/delete_wishlist_flutter', views.delete_wishlist_flutter, name='delete_wishlist_flutter'),
]