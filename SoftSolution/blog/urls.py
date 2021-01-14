from django.urls import path
from .views import Homeview, About, PostCreateView


urlpatterns = [
    path('', Homeview.as_view(), name='blog-home'),
    path('about/', About, name="blog-about"),
    path('post/create/', PostCreateView.as_view(), name="post-create"),

]