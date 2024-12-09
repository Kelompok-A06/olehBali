
# userprofile/views.py

import base64
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserProfileForm, DeleteAccountForm
from .models import Profile
from authentication.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from wishlist.models import Wishlist
import os
import json
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile


@login_required
def dashboard(request, id):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.username,  
            'email': request.user.email,    
        }
    )
    
    if request.user.role == 'user':
        show_wishlist = True
    else: 
        show_wishlist = False
    
    context = {
        'profile': profile,
        'show_wishlist': show_wishlist,
    }
    return render(request, 'dashboard.html', context)


def dashboard_flutter(request, id):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.username,
            'email': request.user.email,
        }
    )
    
    if request.user.role == 'user':
        show_wishlist = True
    else:
        show_wishlist = False
    
    serialized_user = serializers.serialize('json', [request.user])
    serialized_profile = serializers.serialize('json', [profile])
    
    return JsonResponse({
        "user": json.loads(serialized_user),
        "profile": json.loads(serialized_profile),
        "show_wishlist": show_wishlist
    }, status=200)


@login_required
@csrf_exempt
def update_profile(request, id):
    if request.method == 'POST':
        try:
            profile, created = Profile.objects.get_or_create(
                user=request.user,
                defaults={
                    'name': request.POST.get('name', ''),
                    'phone_number': request.POST.get('phone_number', ''),
                    'email': request.POST.get('email', ''),
                    'birthdate': request.POST.get('birthdate', None),
                }
            )

            if not created:
                profile.name = request.POST.get('name', profile.name)
                profile.phone_number = request.POST.get('phone_number', profile.phone_number)
                profile.email = request.POST.get('email', profile.email)
                profile.birthdate = request.POST.get('birthdate', profile.birthdate)

            if request.FILES.get('avatar'):
                profile.avatar = request.FILES['avatar']
            
            profile.save()
            
            response_data = {
                'status': 'success',
                'message': 'Profile updated successfully',
                'data': {
                    'name': profile.name,
                    'phone_number': profile.phone_number,
                    'email': profile.email,
                    'birthdate': profile.birthdate,
                    'avatar_url': profile.avatar.url if profile.avatar else None
                }
            }
            return JsonResponse(response_data)
        
        except Exception as e:
            return JsonResponse({
                'status': 'error', 
                'message': str(e),
                'errors': {
                    'general': 'Failed to update profile. Please try again.'
                }
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def get_user_role(request):
    return JsonResponse({
        'role': request.user.role  
    })

def get_profile(request):
    try:
        profile, created = Profile.objects.get_or_create(
            user=request.user,
            defaults={
                'name': request.user.username,
                'email': request.user.email,
                'phone_number': '',
                'birthdate': None
            }
        )
        
        # Return the profile (either existing or newly created)
        return HttpResponse(
            serializers.serialize("json", [profile]), 
            content_type="application/json"
        )
    except Profile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Profile not found'}, status=404)


@login_required
@csrf_exempt
def update_profile_flutter(request):
    if request.method == 'POST':
        try:
            profile, created = Profile.objects.get_or_create(
                user=request.user,
                defaults={
                    'name': request.user.username,
                    'phone_number': '',
                    'email': request.user.email,
                    'birthdate': None,
                }
            )

            data = json.loads(request.body)
            
            if 'name' in data:
                profile.name = data['name']
            if 'phone_number' in data:
                profile.phone_number = data['phone_number']
            if 'email' in data:
                profile.email = data['email']
            if 'birthdate' in data:
                profile.birthdate = data['birthdate']
            if 'avatar' in data:
                format, imgstr = data['avatar'].split(';base64,') if ';base64,' in data['avatar'] else ('', data['avatar'])
                ext = format.split('/')[-1] if format else 'jpg'
                
                file_name = f'avatar_{request.user.id}.{ext}'
            
                data = ContentFile(base64.b64decode(imgstr), name=file_name)
                profile.avatar.save(file_name, data, save=False)
            
            profile.save()
            
            response_data = {
                'status': 'success',
                'message': 'Profile updated successfully',
                'data': {
                    'name': profile.name,
                    'phone_number': profile.phone_number,
                    'email': profile.email,
                    'birthdate': profile.birthdate,
                    'avatar': profile.avatar.url if profile.avatar else '',
                }
            }
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
                'errors': {
                    'general': 'Failed to update profile. Please try again.'
                }
            }, status=400)
    
    return JsonResponse({
        'status': 'error', 
        'message': 'Invalid request method'
    }, status=400)

def show_user(request, id):
    user = Profile.objects.filter(pk = id);
    return HttpResponse(serializers.serialize("json", user), content_type="application/json")


@login_required
def delete_account(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)

            if data.get('confirm'):  
                user = request.user
                logout(request)  
                user.delete()  
                return JsonResponse({
                    'status': 'success',
                    'redirect_url': reverse_lazy('authentication:login_register')
                }, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Confirmation required.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'status': 'method_not_allowed'}, status=405)

@csrf_exempt
def delete_account_flutter(request):
    if request.method == 'POST': 
        try:
            data = json.loads(request.body)

            if data.get('confirm'):  
                user = request.user
                logout(request)
                user.delete()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Account successfully deleted',
                    'redirect_url': str(reverse_lazy('authentication:login_register'))
                }, status=200)
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Confirmation required.'
                }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error', 
                'message': 'Invalid JSON data.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed'
        }, status=405)