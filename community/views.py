import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Function untuk menampilkan daftar posting
def post_list(request):
    #posts = Post.objects.all().order_by('-created_at')
    posts = Post.objects.all()
    return render(request, 'community/post_list.html', {'posts': posts})

# Function untuk menampilkan detail posting beserta komentar
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            if request.is_ajax():
                return JsonResponse({'success': True, 'comment': comment.content, 'author': comment.author.username})
        else:
            return JsonResponse({'success': False})

    else:
        comment_form = CommentForm()

    return render(request, 'community/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

# Function untuk membuat posting baru
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'community/create_post.html', {'form': form})

# Function untuk menghapus komentar (dengan method POST)
@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
        return JsonResponse({'success': True, 'message': 'Comment deleted successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'You are not allowed to delete this comment.'}, status=403)

# Function untuk menampilkan data dalam format JSON
@login_required
def show_json(request):
    data = Post.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Function untuk menampilkan data dalam format XML
@login_required
def show_xml(request):
    data = Post.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Function untuk menampilkan data JSON berdasarkan ID post
@login_required
def show_json_by_id(request, post_id):
    data = Post.objects.filter(pk=post_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Function untuk menampilkan data XML berdasarkan ID post
@login_required
def show_xml_by_id(request, post_id):
    data = Post.objects.filter(pk=post_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Function untuk menampilkan daftar komentar dalam format JSON
@login_required
def show_comments_json(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    return HttpResponse(serializers.serialize("json", comments), content_type="application/json")

# Function untuk menampilkan daftar komentar dalam format XML
@login_required
def show_comments_xml(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    return HttpResponse(serializers.serialize("xml", comments), content_type="application/xml")

# Function untuk mendaftarkan pengguna baru
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)

# Function untuk login pengguna
def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("post_list"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

# Function untuk logout pengguna
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('login'))
    response.delete_cookie('last_login')
    return response
