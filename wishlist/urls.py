from django.urls import path
from authentication.views import *
from wishlist.views import *
from . import views

app_name = 'wishlist'
urlpatterns =[
    path('', show_wishlist, name='show_wishlist'),
    path('delete-wishlist/<int:id>', views.delete_wishlist, name="delete_wishlist"),
]