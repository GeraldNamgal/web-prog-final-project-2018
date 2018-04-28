from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.apps import apps
from datetime import datetime

# Import models
# from .models import Item

def index(request):
    # If user is not signed in
    if not request.user.is_authenticated:
        return render(request, 'tools/login.html', {'message': None})

    # If user is signed in, get their info
    context = {
        'user': request.user
    }

    # Return index page
    return render(request, 'tools/index.html', context)

def loginView(request):
    if request.method == 'GET':
        return render(request, 'tools/login.html', {'message': None})

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'tools/login.html', {'message': 'Invalid credentials.'})

def register(request):
    if request.method == 'GET':
        return render(request, 'tools/register.html', {'message': None})

    if request.method == 'POST':
        # Error check user input
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            return render(request, 'tools/register.html', {'message': 'Username already exists.'})

        # Process user input
        else:
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            email = request.POST['emailAddress']
            password = request.POST['password']

            # Save user in database
            user = User.objects.create_user(username, email, password)
            user.first_name = firstName
            user.last_name = lastName
            user.save()

            return HttpResponseRedirect(reverse('index'))

def logoutView(request):
    logout(request)
    return render(request, 'tools/login.html', {'message': 'Logged out.'})
