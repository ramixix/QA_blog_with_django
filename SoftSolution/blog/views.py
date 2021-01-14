from django.shortcuts import render

# Create your views here.

def Homeview(request):
    return render(request, 'blog/home.html')

def About(request):
    return render(request, 'blog/about.html')