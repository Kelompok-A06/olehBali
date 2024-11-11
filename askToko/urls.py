from django.urls import path
from . import views

urlpatterns = [
    path('', views.ask_toko, name='ask_toko'),
    path('questions/create/', views.create_question, name='create_question'),
    path('questions/read/', views.read_questions, name='read_questions'),
    path('questions/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('questions/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('questions/<int:question_id>/answers/create/', views.create_answer, name='create_answer'),
    path('questions/<int:question_id>/answers/', views.read_answers, name='read_answers'),
    path('answers/<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),
    path('data/json/', views.show_json, name='show_json'),
    path('data/json/<int:question_id>/', views.show_json_by_id, name='show_json_by_id'),
]
