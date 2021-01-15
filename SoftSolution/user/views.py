from django.shortcuts import render
from django.views.generic import CreateView
from .forms import SingupForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

# Create your views here.
class RegisterView(SuccessMessageMixin, CreateView):
    form_class = SingupForm
    template_name = "user/register.html"
    success_url = reverse_lazy('login')
    success_message = "Your account has been registered successfully, Now You Can Log In!"
