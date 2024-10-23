from django.urls import path
from authentication.views import login_register, logout_user

app_name = 'authentication'

urlpatterns = [
    path('', login_register, name='login_register'),
    path('login/', login_register, name='login_register'),
    path('logout/', logout_user, name='logout'),
]
