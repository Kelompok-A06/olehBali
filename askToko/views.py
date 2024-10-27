from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Answer
from django.utils import timezone

# --- CRUD for Questions ---

@csrf_exempt
def create_question(request):
    if request.method == 'POST' and request.user.is_authenticated:
        question_text = request.POST.get('question')
        question = Question.objects.create(author=request.user, question=question_text, created_at=timezone.now())
        return JsonResponse({'success': True, 'question_id': question.id})
    return JsonResponse({'success': False}, status=400)


def read_questions(request):
    questions = Question.objects.all().order_by('-created_at')[:10]
    questions_data = serializers.serialize('json', questions)
    return JsonResponse({'questions': questions_data})


@csrf_exempt
def edit_question(request, question_id):
    if request.method == 'POST' and request.user.is_authenticated:
        question = get_object_or_404(Question, id=question_id, author=request.user)
        question.question = request.POST.get('question')
        question.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


@csrf_exempt
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id, author=request.user)
    question.delete()
    return JsonResponse({'success': True})


# --- CRUD for Answers (Owners Only) ---

@csrf_exempt
def create_answer(request, question_id):
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_owner:
        question = get_object_or_404(Question, id=question_id)
        answer_text = request.POST.get('answer')
        answer = Answer.objects.create(comment=question, author=request.user, answer=answer_text, created_at=timezone.now())
        return JsonResponse({'success': True, 'answer_id': answer.id})
    return JsonResponse({'success': False}, status=400)


def read_answers(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = question.answers.all().order_by('-created_at')[:4]
    answers_data = serializers.serialize('json', answers)
    return JsonResponse({'answers': answers_data})


@csrf_exempt
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id, author=request.user)
    answer.delete()
    return JsonResponse({'success': True})


# --- Utility Views for JSON and XML data ---

def show_json(request):
    questions = Question.objects.all()
    questions_data = serializers.serialize('json', questions)
    return JsonResponse({'data': questions_data})


def show_json_by_id(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question_data = serializers.serialize('json', [question])
    return JsonResponse({'data': question_data})
