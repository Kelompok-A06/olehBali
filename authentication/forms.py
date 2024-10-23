from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
   ROLE_CHOICES = (
      ('user', 'User'),
      ('admin', 'Admin'),
      ('owner', 'Owner'),
   )

   role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

   class Meta:
      model = User
      fields = ['username', 'password1', 'password2', 'role']
      
