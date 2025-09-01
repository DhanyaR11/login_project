from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not password or not confirm_password:
            messages.error(request, "All fields are required.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match ❌")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken 😢")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created! 🎉 Please login.")
            return redirect("login")

    # IMPORTANT: point to temaccounts/signup.html (not login)
    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}! 🎉")
            return redirect("home")  # we’ll add a proper homepage later
        else:
            messages.error(request, "Invalid username or password ❌")

    return render(request, "accounts/login.html")

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def home_view(request):
    return render(request, "accounts/home.html")

def logout_view(request):
    logout(request)
    return redirect("login")

