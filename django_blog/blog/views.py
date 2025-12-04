# blog/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, PostForm
from .models import Post


# ----------------------------
# AUTHENTICATION VIEWS
# ----------------------------

def register_view(request):
    """Handle user registration."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in immediately after registration
            return redirect("profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


def login_view(request):
    """Handle user login."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = AuthenticationForm()
    return render(request, "blog/login.html", {"form": form})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return render(request, "blog/logout.html")


@login_required
def profile_view(request):
    """Allow authenticated users to view and update their profile."""
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
        return redirect("profile")
    return render(request, "blog/profile.html", {"user": request.user})


# ----------------------------
# BLOG POST CRUD VIEWS
# ----------------------------

class PostListView(ListView):
    """Display all blog posts."""
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10  # optional pagination


class PostDetailView(DetailView):
    """Display a single blog post."""
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    """Allow authenticated users to create a new post."""
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allow authors to edit their own posts."""
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow authors to delete their own posts."""
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        return self.get_object().author == self.request.user
