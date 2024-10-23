from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', show_main, name='home'),
    path('login/', login_register, name='login_register'),
    path('logout/', logout_user, name='logout'),
]
