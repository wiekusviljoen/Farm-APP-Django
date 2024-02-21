from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.
def user_login(request): 
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

def show_user(request):
    print(request.user.username)
    return render(request, 'authentication/user.html', {
        "username": request.user.username,
        "password": request.user.password
    })





    # yourapp/views.py
from django.shortcuts import render, redirect
#from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
            
            
            # Create a new user
            #user = User.objects.create_user(username=username, password=password, first_name=first_name)

            # Optionally, you can log in the user after registration
            

    context = {'form': form}
    

    return render(request, 'authentication/register.html', context)
