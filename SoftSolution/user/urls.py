from django.urls import path
from .views import RegisterView, Profile

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-registration'),
    path('profile/', Profile, name='profile'),

]