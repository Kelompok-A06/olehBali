from django.urls import path
from userprofile.views import login_register, logout_user

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
]