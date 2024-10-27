from django.urls import path
from community.views import *

app_name = 'community'

urlpatterns = [
    path('', post_list, name='post_list'),  # Menampilkan daftar semua post
    path('post/<int:post_id>/', post_detail, name='post_detail'),  # Detail post berdasarkan ID
    path('post/create/', create_post, name='create_post'),  # Membuat post baru
    path('post/<int:post_id>/json/', show_json_by_id, name='show_json_by_id'),  # Post dalam format JSON berdasarkan ID
    path('post/<int:post_id>/xml/', show_xml_by_id, name='show_xml_by_id'),  # Post dalam format XML berdasarkan ID
    path('post/<int:post_id>/comments/json/', show_comments_json, name='show_comments_json'),  # Komentar post dalam format JSON
    path('post/<int:post_id>/comments/xml/', show_comments_xml, name='show_comments_xml'),  # Komentar post dalam format XML
    path('post/json/', show_json, name='show_json'),  # Semua post dalam format JSON
    path('post/xml/', show_xml, name='show_xml'),  # Semua post dalam format XML
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),  # Menghapus post berdasarkan ID
    path('post/<int:post_id>/comments/', get_comments, name='get_comments'),  # Mendapatkan semua komentar dari post
    path('post/<int:post_id>/comments/create/', create_comment, name='create_comment'),  # Menambahkan komentar pada post
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'), # Menghapus komentar berdasarkan ID
    path('post/<int:post_id>/update/', update_post, name='update_post'),  # Mengupdate post berdasarkan ID
]
