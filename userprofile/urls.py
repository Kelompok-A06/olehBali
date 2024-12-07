from django.conf import settings
from django.urls import path
from .views import *
from django.conf.urls.static import static


app_name = 'userprofile'

urlpatterns = [
    path('dashboard/<int:id>/', dashboard, name='dashboard'),
    path('api/profile/', get_profile, name='get_profile'),
    path('dashboard_flutter/<int:id>/', dashboard_flutter, name='dashboard_flutter'),
    path('update-profile/<int:id>/', update_profile, name='update_profile'),
    path('update_profile_flutter/<int:id>/', update_profile_flutter, name='update_profile_flutter'),
    path('delete-account/', delete_account, name='delete_account'),
    path('delete_account_flutter/', delete_account_flutter, name='delete_account_flutter'),
    path('json/<int:id>', show_user, name='show_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)