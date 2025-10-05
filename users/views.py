from .forms import CustomUserCreationForm, EmailAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth import get_user_model
from reviews.models import Review
from django.http import JsonResponse

User = get_user_model()

def all_user_ids():
    """Return a list of all user IDs in the database."""
    return list(User.objects.values_list('id', flat=True))

def user_ids_debug(request):
    """Return all user IDs as JSON (for debugging)."""
    ids = all_user_ids()
    return JsonResponse({'user_ids': ids})

def print_all_user_ids():
    """Print all user IDs to the console (for debugging)."""
    ids = all_user_ids()
    print("All user IDs:", ids)

def register(request):
    if request.user.is_authenticated:
        return redirect("home")  # Redirect to home if already logged in

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("success")  # Redirect to success page with link to login
    else:
        form = CustomUserCreationForm()  # Returns an unbound form (empty form for user input)
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")  # Redirect to home if already logged in

    if request.method == "POST":
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = EmailAuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def success(request):
    # Example: show all user IDs on the success page
    return render(request, "users/success.html", {"user_ids": all_user_ids()})

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    reviews = Review.objects.filter(user=profile_user).order_by('-created')
    is_following = request.user.following.filter(pk=profile_user.pk).exists()
    return render(request, "users/profile.html", {
        "profile_user": profile_user,
        "reviews": reviews,
        "is_following": is_following,
    })

@login_required
def follow_user(request, pk):
    to_follow = get_object_or_404(User, pk=pk)
    if to_follow != request.user:
        request.user.following.add(to_follow)
    return redirect('profile', pk=pk)

@login_required
def unfollow_user(request, pk):
    to_unfollow = get_object_or_404(User, pk=pk)
    if to_unfollow != request.user:
        request.user.following.remove(to_unfollow)
    # Redirect to the logged-in user's own profile page
    return redirect('profile', pk=request.user.pk)

@login_required
def user_search(request):
    query = request.GET.get("search", "")
    results = []
    if query:
        results = User.objects.filter(
            models.Q(username__contains=query) |
            models.Q(first_name__contains=query) |
            models.Q(last_name__contains=query)
        )
    return render(request, "users/user_search.html", {"query": query, "results": results})