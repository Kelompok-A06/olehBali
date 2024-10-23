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
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def show_main(request):
    context = {}
    return render(request, "home.html", context)

def login_register(request):
    login_form = AuthenticationForm()  # Always show a fresh login form
    register_form = CustomUserCreationForm()  # Always show a fresh registration form
    
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(data=request.POST) 
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('authentication:home') 
            else:
                messages.error(request, "Invalid username or password. Please try again.")
        
        elif 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)  
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Your account has been successfully created!')
                return redirect('authentication:login_register') 
            else:
                for error in register_form.non_field_errors():
                    messages.error(request, error)
    
    context = {
        'login_form': login_form,  
        'register_form': register_form  
    }
    return render(request, 'login.html', context)



def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login'))
    response.delete_cookie('last_login')
    return response