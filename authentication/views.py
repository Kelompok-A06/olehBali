import datetime
from django.shortcuts import render, redirect, reverse
from userprofile.models import Profile
from .models import User
from .forms import CustomUserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User
from reviews.models import Reviews
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def show_main(request):
    profile = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.username,  
            'email': request.user.email,    
        }
    )

    reviews = Reviews.objects.all()
    context = {
        'user_name': request.user.username,
        'profile' : profile[0],
        'user' : request.user,
        'reviews' : reviews
    }
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
                response = HttpResponseRedirect(reverse("authentication:home"))
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
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
    response = HttpResponseRedirect(reverse('authentication:login_register'))
    response.delete_cookie('last_login')
    return response