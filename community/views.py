import datetime
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment
from .forms import PostForm, CommentForm

@login_required(login_url='/login')
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'community/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    # Ambil post berdasarkan ID
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Ambil komentar untuk post tersebut

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('community:post_detail', post_id=post_id)
    else:
        comment_form = CommentForm()  # Form kosong untuk GET request

    return render(request, 'community/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

def post_detail(request, post_id):
    # Ambil post berdasarkan ID
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Ambil komentar untuk post tersebut

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('community:post_detail', post_id=post_id)
    else:
        comment_form = CommentForm()  # Form kosong untuk GET request

    return render(request, 'community/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        try:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.created_at = timezone.now()
                post.save()

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'post_id': post.id,
                        'title': post.title,
                        'content': post.content,
                        'author': post.author.username,
                        'created_at': post.created_at.strftime('%b %d, %Y %H:%M'),  # Format tanggal yang sesuai dengan frontend
                        'is_author': True,  # Karena ini post baru, user pasti authornya
                    })
                return redirect('community:post_list')
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'Invalid form data',
                        'errors': form.errors
                    }, status=400)
                messages.error(request, "Please correct the errors below.")
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)
            messages.error(request, f"An error occurred: {str(e)}")
    else:
        form = PostForm()
    
    return render(request, 'community/create_post.html', {'form': form})

@login_required
@require_POST
def update_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id, author=request.user)  # Ensure user is the author
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            post.title = title
            post.content = content
            post.save()

            return JsonResponse({'success': True, 'title': title, 'content': content})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid data provided'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
@require_POST
def delete_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        if post.author == request.user:
            post.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Post deleted successfully!'
                })
            messages.success(request, "Post deleted successfully!")
            return redirect('community:post_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'You are not authorized to delete this post.'
                }, status=403)
            messages.error(request, "You are not authorized to delete this post.")
            return redirect('community:post_list')
    except Exception as e:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('community:post_list')

@login_required
@require_POST
def delete_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        
        # Check if the current user is the author of the comment
        if comment.author != request.user:
            return JsonResponse({
                'success': False,
                'error': 'You do not have permission to delete this comment'
            }, status=403)
            
        # Delete the comment
        comment.delete()
        
        return JsonResponse({
            'success': True
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
    
def show_json(request):
    try:
        posts = Post.objects.all().order_by('-created_at')
        post_list = []
        
        for post in posts:
            post_data = {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': post.author.username,
                'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'comments_count': post.comments.count(),
                'is_author': request.user == post.author if request.user.is_authenticated else False
            }
            post_list.append(post_data)
            
        return JsonResponse({
            'status': True,
            'message': 'Successfully fetched all posts',
            'data': post_list
        }, safe=False)
    except Exception as e:
        return JsonResponse({
            'status': False,
            'message': str(e)
        }, status=500)

def show_xml(request):
    data = Post.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Fungsi untuk menampilkan post berdasarkan ID dalam format JSON
def show_json_by_id(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()
        
        comments_data = []
        for comment in comments:
            comment_data = {
                'id': comment.id,
                'content': comment.content,
                'author': comment.author.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            comments_data.append(comment_data)
        
        post_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'comments': comments_data
        }
        
        return JsonResponse({
            'status': True,
            'message': 'Successfully fetched post detail',
            'data': post_data
        })
    except Post.DoesNotExist:
        return JsonResponse({
            'status': False,
            'message': 'Post not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': False,
            'message': str(e)
        }, status=500)
    
@login_required
@require_POST
def create_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')

        if not content:
            return JsonResponse({
                'success': False,
                'error': 'Content is required to create a comment.'
            }, status=400)

        try:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                created_at=timezone.now()
            )

            return JsonResponse({
                'success': True,
                'comment_id': comment.id,
                'content': comment.content,
                'author': comment.author.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }, status=201)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    return JsonResponse({
        'success': False,
        'error': 'Invalid request method.'
    }, status=405)

def get_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    
    comments_data = [{
        'id': comment.id,
        'content': comment.content,
        'author': comment.author.username,
        'created_at': comment.created_at.strftime('%b %d, %Y %H:%M'),
        'is_author': comment.author == request.user
    } for comment in comments]
    
    return JsonResponse(comments_data, safe=False)

def show_xml_by_id(request, post_id):
    data = Post.objects.filter(pk=post_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Fungsi untuk menampilkan semua komentar dari post tertentu dalam format JSON
def show_comments_json(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all().order_by('-created_at')
        
        comments_data = []
        for comment in comments:
            comment_data = {
                'id': comment.id,
                'content': comment.content,
                'author': comment.author.username,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'is_author': request.user == comment.author if request.user.is_authenticated else False
            }
            comments_data.append(comment_data)
        
        return JsonResponse({
            'status': True,
            'message': 'Successfully fetched all comments',
            'data': comments_data
        }, safe=False)
    except Post.DoesNotExist:
        return JsonResponse({
            'status': False,
            'message': 'Post not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': False,
            'message': str(e)
        }, status=500)
    
# Fungsi untuk mendapatkan komentar spesifik berdasarkan ID
def show_comment_by_id(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        
        comment_data = {
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.username,
            'post_id': comment.post.id,
            'post_title': comment.post.title,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_author': request.user == comment.author if request.user.is_authenticated else False
        }
        
        return JsonResponse({
            'status': True,
            'message': 'Successfully fetched comment detail',
            'data': comment_data
        })
    except Comment.DoesNotExist:
        return JsonResponse({
            'status': False,
            'message': 'Comment not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': False,
            'message': str(e)
        }, status=500)
    
def show_comments_xml(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    return HttpResponse(serializers.serialize("xml", comments), content_type="application/xml")

# views.py
@csrf_exempt
@login_required
def create_post_flutter(request):
    if request.method == 'POST':
        try:
            # Cek apakah data dikirim sebagai JSON atau form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            title = data.get('title')
            content = data.get('content')

            # Validate required fields
            if not title or not content:
                return JsonResponse({
                    'status': False,
                    'message': 'Title and content are required fields'
                }, status=400)

            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user,
                created_at=timezone.now()
            )

            # Format response sesuai dengan Post.fromJson di Flutter
            return JsonResponse({
                'status': True,
                'message': 'Post created successfully',
                'data': {
                    'id': post.id,
                    'title': post.title,
                    'content': post.content,
                    'author': post.author.username,
                    'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'comments_count': post.comments.count(),
                    'is_author': True  # Karena post baru dibuat oleh user yang sedang login
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({
                'status': False,
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': False,
        'message': 'Method not allowed'
    }, status=405)

@csrf_exempt
@login_required
def create_comment_flutter(request, post_id):
    if request.method == 'POST':
        try:
            post = get_object_or_404(Post, id=post_id)
            
            # Handle both JSON and form data
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    data = request.POST
            else:
                data = request.POST
                
            content = data.get('content')

            if not content:
                return JsonResponse({
                    'status': False,
                    'message': 'Content is required'
                }, status=400)

            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                created_at=timezone.now()
            )

            return JsonResponse({
                'status': True,
                'message': 'Comment created successfully',
                'data': {
                    'id': comment.id,
                    'content': comment.content,
                    'author': comment.author.username,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'post_id': post.id
                }
            }, status=201)

        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': False,
        'message': 'Method not allowed'
    }, status=405)

@csrf_exempt
@login_required
def delete_post_flutter(request, post_id):
    if request.method in ['DELETE', 'POST']:
        try:
            post = get_object_or_404(Post, id=post_id)
            
            # Check if user is the author
            if post.author != request.user:
                return JsonResponse({
                    'status': False,
                    'message': 'You are not authorized to delete this post'
                }, status=403)

            post.delete()
            return JsonResponse({
                'status': True,
                'message': 'Post deleted successfully'
            })

        except Post.DoesNotExist:
            return JsonResponse({
                'status': False,
                'message': 'Post not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': False,
        'message': 'Method not allowed'
    }, status=405)

@csrf_exempt
@login_required
def delete_comment_flutter(request, comment_id):
    if request.method in ['DELETE', 'POST']:  # Accept both DELETE and POST
        try:
            comment = get_object_or_404(Comment, id=comment_id)
            
            # Check if user is the author
            if comment.author != request.user:
                return JsonResponse({
                    'status': False,
                    'message': 'You are not authorized to delete this comment'
                }, status=403)

            comment.delete()
            return JsonResponse({
                'status': True,
                'message': 'Comment deleted successfully'
            })

        except Exception as e:
            return JsonResponse({
                'status': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': False,
        'message': 'Method not allowed'
    }, status=405)