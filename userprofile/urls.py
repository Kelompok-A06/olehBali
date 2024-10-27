from django.urls import path
from .views import *

app_name = 'userprofile'

urlpatterns = [
    path('dashboard/<int:id>/', dashboard, name='dashboard'),
    path('update-profile/<int:id>/', update_profile, name='update_profile'),
    path('delete-account/', delete_account, name='delete_account'),
    path('json/<int:id>', show_user, name='show_user'),

]