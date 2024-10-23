import datetime
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from .models import User
from .forms import CustomUserCreationForm

# Create your views here.

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User
from .forms import CustomUserCreationForm

def login_register(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('home:dashboard')  # Redirect to the dashboard after login
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        
        elif 'register' in request.POST:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                account = form.save(commit=False)
                account.role = form.cleaned_data['role']
                account.save()
                messages.success(request, 'Your account has been successfully created!')
                return redirect('authentication:login')  # Redirect to the login form after registration
    else:
        form = AuthenticationForm()

    context = {
        'login_form': AuthenticationForm(),  # Always show a fresh login form
        'register_form': CustomUserCreationForm()  # Always show a fresh registration form
    }
    return render(request, 'login.html', context)



def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login'))
    response.delete_cookie('last_login')
    return response