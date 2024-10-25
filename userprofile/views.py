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
    # Coba untuk mendapatkan profile terkait user
    try:
        profile = Profile.objects.get(pk=id)
    except Profile.DoesNotExist:
        profile = None
        
    if profile is None:
        form = UserProfileForm(request.POST or None)
        if form.is_valid() and request.method == "POST":
            profile_entry= form.save(commit=False)
            profile_entry.user = request.user
            profile_entry.save()
            return redirect('authentication:home')
    else:
        form = UserProfileForm(request.POST or None, instance=profile)
        if form.is_valid() and request.method == "POST":
            form.save()
            return HttpResponseRedirect(reverse('authentication:home'))
        
    if request.user.role == 'user':
        show_wishlist = True
    else: 
        show_wishlist = False
    
    context = {
        'profile': profile,
        'show_wishlist': show_wishlist,
    }
    return render(request, 'dashboard.html', context)

def show_user(request, id):
    user = Profile.objects.filter(pk = id);
    return HttpResponse(serializers.serialize("json", user), content_type="application/json")

# @login_required
# def edit_profile(request):
#     profile = get_object_or_404(Profile, user=request.user)

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()

#             # If avatar is updated, get its URL
#             avatar_url = profile.avatar.url if profile.avatar else ''
            
#             return JsonResponse({
#                 'status': 'success',
#                 'name': profile.name,
#                 'phone': profile.phone,
#                 'email': profile.email,
#                 'birthdate': profile.birthdate.strftime('%Y-%m-%d'),
#                 'avatar_url': avatar_url,
#             })
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid form submission'})
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
# @login_required
# def edit_profile(request):
#     # Mengambil atau membuat profile baru jika belum ada
#     profile, created = Profile.objects.get_or_create(user=request.user)
    
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully.')
#             return redirect('userprofile:dashboard', id=profile.id)
#     else:
#         form = UserProfileForm(instance=profile)
    
#     context = {
#         'form': form,
#     }
#     return render(request, 'edit_profile.html', context)

# @login_required
# @csrf_exempt
# def update_profile(request, id):
#     profile = get_object_or_404(Profile, user=request.user)

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()

#             # If avatar is updated, get its URL
#             avatar_url = profile.avatar.url if profile.avatar else ''
            
#             return JsonResponse({
#                 'status': 'success',
#                 'name': profile.name,
#                 'phone': profile.phone,
#                 'email': profile.email,
#                 'birthdate': profile.birthdate.strftime('%Y-%m-%d'),
#                 'avatar_url': avatar_url,
#             })
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid form submission'})
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# @login_required
# @csrf_exempt
# def update_profile(request, id):
#     if request.method == 'POST':
#         try:
#             profile = Profile.objects.get(pk=id)
            
#             # Handle file upload
#             if request.FILES.get('avatar'):
#                 profile.avatar = request.FILES['avatar']
            
#             # Update other fields
#             profile.name = request.POST.get('name')
#             profile.phone_number = request.POST.get('phone_number')
#             profile.email = request.POST.get('email')
#             profile.birthdate = request.POST.get('birthdate')
            
#             profile.save()
            
#             response_data = {
#                 'status': 'success',
#                 'message': 'Profile updated successfully',
#                 'data': {
#                     'name': profile.name,
#                     'phone_number': profile.phone_number,
#                     'email': profile.email,
#                     'birthdate': profile.birthdate,
#                     'avatar_url': profile.avatar.url if profile.avatar else None
#                 }
#             }
#             return JsonResponse(response_data)
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@login_required
@csrf_exempt
def update_profile(request, id):
    if request.method == 'POST':
        try:
            # Coba untuk mendapatkan profil berdasarkan id
            try:
                profile = Profile.objects.get(pk=id)
            except Profile.DoesNotExist:
                # Buat profil baru jika belum ada
                profile = Profile(user=request.user)

            # Handle file upload jika ada
            if request.FILES.get('avatar'):
                profile.avatar = request.FILES['avatar']
            
            # Update kolom lain
            profile.name = request.POST.get('name', profile.name)
            profile.phone_number = request.POST.get('phone_number', profile.phone_number)
            profile.email = request.POST.get('email', profile.email)
            profile.birthdate = request.POST.get('birthdate', profile.birthdate)
            
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
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# @login_required
# def edit_profile(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True, 'message': 'Profile updated successfully.', 'data': {
#                 'name': form.cleaned_data['name'],
#                 'phone_number': form.cleaned_data['phone_number'],
#                 'email': form.cleaned_data['email'],
#                 'birthdate': form.cleaned_data['birthdate'],
#                 'avatar': form.cleaned_data['avatar'].url if form.cleaned_data['avatar'] else None
#             }})
#         else:
#             return JsonResponse({'success': False, 'errors': form.errors}, status=400)
#     else:
#         form = UserProfileForm(instance=profile)

#     context = {
#         'form': form,
#         'profile': profile
#     }
#     return render(request, 'edit_profile.html', context)



# @login_required
# def delete_account(request):
#     if request.method == 'POST':
#         form = DeleteAccountForm(request.POST)
#         if form.is_valid() and form.cleaned_data['confirm']:
#             user = request.user
#             logout(request)
#             user.delete()
#             messages.success(request, 'Account deleted successfully.')
#             return redirect('authentication:login')
#     else:
#         form = DeleteAccountForm()
    
#     context = {
#         'form': form,
#     }
#     return JsonResponse({'status': 'method_not_allowed'}, status=405)

# INI HAMPIR BENER
# @login_required
# @csrf_exempt
# def update_profile(request, id):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         try:
#             profile = Profile.objects.get(pk=id)
            
#             # Handle file upload
#             if request.FILES.get('avatar'):
#                 profile.avatar = request.FILES['avatar']
            
#             # Update other fields
#             profile.name = request.POST.get('name')
#             profile.phone_number = request.POST.get('phone_number')
#             profile.email = request.POST.get('email')
#             profile.birthdate = request.POST.get('birthdate')
            
#             profile.save()
            
#             response_data = {
#                 'status': 'success',
#                 'message': 'Profile updated successfully',
#                 'data': {
#                     'name': profile.name,
#                     'phone_number': profile.phone_number,
#                     'email': profile.email,
#                     'birthdate': profile.birthdate,
#                     'avatar_url': profile.avatar.url if profile.avatar else None
#                 }
#             }
#             return JsonResponse(response_data)
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)



@login_required
def delete_account(request):
    if request.method == 'DELETE':
        try:
            # Load JSON data from request body
            data = json.loads(request.body)

            if data.get('confirm'):  # Check if confirmation is provided
                user = request.user
                logout(request)  # Log the user out
                user.delete()  # Delete the user
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
