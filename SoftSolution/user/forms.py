from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SingupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=128, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2' ]

