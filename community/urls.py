from django.urls import path
from . import views
app_name = 'community'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/json/', views.show_json_by_id, name='show_json_by_id'),
    path('post/<int:post_id>/xml/', views.show_xml_by_id, name='show_xml_by_id'),
    path('post/<int:post_id>/comments/json/', views.show_comments_json, name='show_comments_json'),
    path('post/<int:post_id>/comments/xml/', views.show_comments_xml, name='show_comments_xml'),
    path('post/json/', views.show_json, name='show_json'),
    path('post/xml/', views.show_xml, name='show_xml'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
