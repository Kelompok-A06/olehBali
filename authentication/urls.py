from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', show_main, name='home'),
    path('login/', login_register, name='login_register'),
    path('logout/', logout_user, name='logout'),
    path('login-flutter/', login_flutter, name='login_flutter'),
    path('register-flutter/', register_flutter, name='register_flutter'),
    path('logout-flutter/', logout_flutter, name='logout_flutter'),
]
