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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


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
                messages.error(request, "Invalid username or password. Please try again.", extra_tags="auth")
        
        elif 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)  
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Your account has been successfully created!', extra_tags="auth")
                return redirect('authentication:login_register') 
            else:
                for error in register_form.non_field_errors():
                    messages.error(request, error)
    
    context = {
        'login_form': login_form,  
        'register_form': register_form  
    }
    return render(request, 'login.html', context)

@csrf_exempt
def login_flutter(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "role": user.role,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt
def register_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        role = data['role']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1, role=role)
        user.save()
        
        return JsonResponse({
            "username": user.username,
            "role" : user.role,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
    
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:login_register'))
    response.delete_cookie('last_login')
    return response