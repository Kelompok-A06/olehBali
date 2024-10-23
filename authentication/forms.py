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
      
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Your password must be at least 8 characters long and should not be entirely numeric."
        self.fields['password2'].help_text = "Enter the same password as before, for verification."
