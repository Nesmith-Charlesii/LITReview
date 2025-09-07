from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect


def register(request):
    if request.user.is_authenticated:
        return redirect("home") # Redirect to their profile page if already logged in

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("success")  # Redirect to success page with link to login
    else:
        form = CustomUserCreationForm() # What does this return by default without any arguments?
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home") # Redirect to their profile page if already logged in

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def success(request):
    return render(request, "users/success.html")

def logout_view(request):
    logout(request)
    return redirect("home")