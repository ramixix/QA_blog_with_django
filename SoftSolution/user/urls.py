from django.urls import path
from .views import Register, Profile

urlpatterns = [
    path('register/', Register, name='user-registration'),
    path('profile/', Profile, name='profile'),

]