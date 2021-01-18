from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import SingupForm, UserUpdateForm, ProfileUpdateForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required       # an decoder to make sure that user is login before opening profile view
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

# class for register view 
def Register(request):
    form = SingupForm()
    if request.method == 'POST':

        form = SingupForm(request.POST)
        email = request.POST['email']
        emails = User.objects.filter(is_active=True).values_list('email', flat=True)

        if email in emails:
            form.add_error(None,'This email is already exists')
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Has been created succesfully")
            return redirect('login')

    context ={'form':form}
    return render(request,'user/register.html',context)

# function to handles the post and get request to profile page, if the request is post it is going to examine if the post form
# is valid and if its then it is going to be save to database and redirect user to that profile page
@login_required
def Profile(request):
    if request.method == 'POST':
        # if the method is post then take two forms and pass the form to them
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        # see if forms are valid and if its save them and send a succcess message and finally redirect user to that profile page
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # use the class we import above this is going to add our specified message to message list and we can use it in base.html to display them
            messages.success(request, "Your Informations Has Been Updated Successfully")
            return redirect('profile')
    else:
        # if method is not post then it is going to be get, in that situation two froms will pass empty
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)


    context = { 'user_form' : user_form, 'profile_form' : profile_form }
    return render(request, "user/profile.html", context)