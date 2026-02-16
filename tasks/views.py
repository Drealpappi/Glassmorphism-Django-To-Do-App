from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    task = Task.objects.all()
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/")
    
    context = {
        "tasks": task,
        "form": form
    }
    return render(request, "tasks/list.html", context)

def update_task(request, pk):
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect("/")
    
    context = {
        "form": form,
        "task": task
    }
    return render(request, "tasks/update_task.html", context)

@login_required(login_url='login')
def list_tasks(request):
    # This is the "Magic" line that separates the accounts:
    tasks = Task.objects.filter(user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            # Before saving, we "attach" the current user to the task
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('list')
    else:
        form = TaskForm()

    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context)

def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    
    context = {
        "task": task
    }
    return render(request, "tasks/delete.html", context)

def register(request):
    if request.method == "POST":
    
        email = request.POST["email"]
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        # Create user (uses email as username)
        user = User.objects.create_user(username=email, email=email, password=password1)
        messages.success(request, "Account created successfully")
        return redirect("login")
    return render(request, "tasks/register.html")

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password =request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request=request, user=user)
            return redirect("/")
        else:
            messages.info(request, "Invalid credentials")
            return redirect("login")
    return render(request, "tasks/login.html")


def logout_user(request):
    auth_logout(request)
    return redirect('login')