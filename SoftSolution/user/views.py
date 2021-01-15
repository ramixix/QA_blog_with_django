from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import SingupForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

class RegisterView(SuccessMessageMixin, CreateView):
    form_class = SingupForm
    template_name = "user/register.html"
    success_url = reverse_lazy('login')
    success_message = "Your account has been registered successfully, Now You Can Log In!"

@login_required
def Profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Informations Has Been Updated Successfully")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)


    context = { 'user_form' : user_form, 'profile_form' : profile_form }
    return render(request, "user/profile.html", context)