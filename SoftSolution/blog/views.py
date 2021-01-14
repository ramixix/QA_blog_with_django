from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import ListView

# Create your views here.

class Homeview(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = 'posts'
    ordering = ["-date_posted"]

def About(request):
    return render(request, 'blog/about.html')