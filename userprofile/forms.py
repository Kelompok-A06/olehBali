# user_profile/forms.py

from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone_number', 'email', 'birthdate', 'avatar']

class DeleteAccountForm(forms.Form):
    confirm = forms.BooleanField(label="I confirm that I want to delete my account")