from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# normal form for registeration page 
class SingupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email = forms.EmailField(max_length=128, help_text='Enter a valid email address'
                             ,widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    username= forms.CharField(max_length=120,widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password1 = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'placeholder':'Confirm password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2' ]


# from for profile page and allow users to update their information about user model in their profile page
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email' ]

# from for profile page and allowing users to update their profile model information in their profile page
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'education', 'website_url', 'linkin_url', 'facebook_url', 'image']