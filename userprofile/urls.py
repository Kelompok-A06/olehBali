from django.urls import path
from .views import *

app_name = 'userprofile'

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('edit/', edit_profile, name='edit_profile'),
    path('delete/', delete_account, name='delete_account'),
    path('wishlist/', wishlist_dashboard, name='wishlist_dashboard'),
]