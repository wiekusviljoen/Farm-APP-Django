from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def user_login(request): 
    # Redirect already logged-in users to the farm list
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('farm_app:farm_list'))
    return render(request, 'authentication/login.html')

    


def authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponseRedirect(
            reverse('user_auth:login')
        )
    else:
        login(request, user)
        return HttpResponseRedirect(
            reverse('user_auth:show_user')
        )

@login_required
def show_user(request):
    return render(request, 'authentication/user.html', {
        "username": request.user.username,
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name
    })


@login_required
def logout_user(request):
    """Log out the user and redirect to login page."""
    logout(request)
    return HttpResponseRedirect(reverse('user_auth:login'))





    # yourapp/views.py

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after successful registration
            login(request, user)
            return redirect('farm_app:farm_list')
            

    context = {'form': form}
    

    return render(request, 'authentication/register.html', context)
