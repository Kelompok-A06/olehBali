from django.urls import path
from authentication.views import *
from wishlist.views import *

app_name = 'wishlist'
urlpatterns =[
    path('', show_wishlist, name='show_wishlist'),
    path('delete-wishlist/<int:id>', delete_wishlist, name="delete_wishlist")
]