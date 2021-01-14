from django.urls import path
from .views import Homeview, About, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView


urlpatterns = [
    path('', Homeview.as_view(), name='blog-home'),
    path('about/', About, name="blog-about"),
    path('post/create/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
]