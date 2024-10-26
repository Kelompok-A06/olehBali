
# user_profile/views.py

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserProfileForm, DeleteAccountForm
from .models import Profile
from authentication.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import os
import json
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt


@login_required
def dashboard(request, id):
    # Get or create profile for the current user
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

@login_required
@csrf_exempt
def update_profile(request, id):
    if request.method == 'POST':
        try:
            # Get or create profile
            profile, created = Profile.objects.get_or_create(
                user=request.user,
                defaults={
                    'name': request.POST.get('name', ''),
                    'phone_number': request.POST.get('phone_number', ''),
                    'email': request.POST.get('email', ''),
                    'birthdate': request.POST.get('birthdate', None),
                }
            )

            # Update existing profile
            if not created:
                profile.name = request.POST.get('name', profile.name)
                profile.phone_number = request.POST.get('phone_number', profile.phone_number)
                profile.email = request.POST.get('email', profile.email)
                profile.birthdate = request.POST.get('birthdate', profile.birthdate)

            # Handle avatar upload
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


def show_user(request, id):
    user = Profile.objects.filter(pk = id);
    return HttpResponse(serializers.serialize("json", user), content_type="application/json")


@login_required
def delete_account(request):
    if request.method == 'DELETE':
        try:
            # Load JSON data from request body
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

@login_required
def wishlist_dashboard(request):
    # Placeholder untuk wishlist, nanti disesuaikan dengan model wishlist
    context = {
        "user": request.user
    }
    return render(request, 'wishlist.html', context)
