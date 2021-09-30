from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from foods.models import Category
from .forms import LoginForm
from accounts.auth import unauthenticated_user, admin_only, user_only
from django.contrib.auth.decorators import login_required


# Create your views here.
def homepage(request):
    return render(request, 'accounts/homepage.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('/login')


@unauthenticated_user
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'],
                                password=data['password'])
            # print(user)
            if user is not None:
                if not user.is_staff:
                    login(request, user)
                    return redirect('/')
                elif user.is_staff:
                    login(request, user)
                    return redirect('/admins')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid username or password')
                return render(request, 'accounts/login.html', {'form_login': form})
    context = {
        'activate_login': 'active',
        'form_login': LoginForm
    }
    return render(request, 'accounts/login.html', context)


@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Profile.objects.create(user=user, username=user.username, email=user.email)

            messages.add_message(request, messages.SUCCESS, 'User registered successfully')
            return redirect('/login')
        else:
            messages.add_message(request, messages.ERROR, 'unable to register user')
            return render(request, 'accounts/register.html', {'form_register': form})
    context = {
        'form_register': UserCreationForm,
        'activate_register': 'active'
    }
    return render(request, 'accounts/register.html', context)
