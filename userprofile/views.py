# user_profile/views.py

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from .forms import UserProfileForm, DeleteAccountForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


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


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('userprofile:dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
    }
    return render(request, 'userprofile/edit_profile.html', context)

@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, 'Account deleted successfully.')
            return redirect('authentication:login_register')
    else:
        form = DeleteAccountForm()
    
    context = {
        'form': form,
    }
    return render(request, 'userprofile/delete_account.html', context)

@login_required
def wishlist_dashboard(request):
    # Placeholder untuk wishlist, nanti disesuaikan dengan model wishlist
    context = {}
    return render(request, 'userprofile/wishlist_dashboard.html', context)
