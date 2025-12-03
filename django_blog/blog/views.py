from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == "POST":
         form = CustomUserCreationForm(request.POST)
         if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect("profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

# Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# Logout
def logout_view(request):
    logout(request)
    return redirect("login")

# Profile
def profile_view(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
    return render(request, "profile.html", {"user": request.user})


