from django.urls import path
from community.views import *

app_name = 'community'

urlpatterns = [
    # Basic web views
    path('', post_list, name='post_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/create/', create_post, name='create_post'),
    path('post/<int:post_id>/update/', update_post, name='update_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    
    # Comments management
    path('post/<int:post_id>/comments/', get_comments, name='get_comments'),
    path('post/<int:post_id>/comments/create/', create_comment, name='create_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    
    # JSON endpoints
    path('json/', show_json, name='show_json'),  # All posts
    path('post/<int:post_id>/json/', show_json_by_id, name='show_json_by_id'),  # Single post
    path('post/<int:post_id>/comments/json/', show_comments_json, name='show_comments_json'),  # Comments for a post
    path('comment/<int:comment_id>/json/', show_comment_by_id, name='show_comment_by_id'),  # Single comment
    
    # XML endpoints
    path('xml/', show_xml, name='show_xml'),  # All posts
    path('post/<int:post_id>/xml/', show_xml_by_id, name='show_xml_by_id'),  # Single post
    path('post/<int:post_id>/comments/xml/', show_comments_xml, name='show_comments_xml'),  # Comments for a post
    
    # Flutter/mobile API endpoints
    path('create-post-flutter/', create_post_flutter, name='create_post_flutter'),
    path('post/<int:post_id>/comment-flutter/', create_comment_flutter, name='create_comment_flutter'),
    path('post/<int:post_id>/delete-flutter/', delete_post_flutter, name='delete_post_flutter'),
    path('comment/<int:comment_id>/delete-flutter/', delete_comment_flutter, name='delete_comment_flutter'),
]