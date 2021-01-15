from django.urls import path
from .views import (Homeview, About, PostCreateView, PostDetailView, PostUpdateView,
                    PostDeleteView, CategoryView, UserProfileView, LikeView, DisLikeView,
                    CommentLikeView, CommentDisLikeView,
                    )


urlpatterns = [
    path('', Homeview.as_view(), name='blog-home'),
    path('about/', About, name="blog-about"),
    path('post/create/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('category/<str:cat>', CategoryView.as_view(), name="blog-category"),
    path('usr/<str:username>/', UserProfileView.as_view(), name="user-profile"),
    path('like/<int:pk>/', LikeView, name="like-post"),
    path('dislike/<int:pk>/', DisLikeView, name="dislike-post"),
    path('comment/<int:pk>/like', CommentLikeView, name="like-comment"),
    path('comment/<int:pk>/dislike', CommentDisLikeView, name="dislike-comment"),
]