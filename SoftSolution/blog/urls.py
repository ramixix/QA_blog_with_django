from django.urls import path
from .views import Homeview, About


urlpatterns = [
    path('', Homeview.as_view(), name='blog-home'),
    path('about/', About, name="blog-about"),

]