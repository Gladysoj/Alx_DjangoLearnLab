# blog/views.py
from django.db.models import Q
from django.forms import PostForm
from .models import Post, Tag 
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import CustomUserCreationForm, PostForm
from .models import Post, CommentForm

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.post
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return redirect(reverse('post-detail', kwargs={'pk': self.post.pk}))  # back to post detail

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.get_object().post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.get_object().post.pk})
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
        response = super().form_valid(form)
        tag_names = form.cleaned_data.get('tags_input', [])
        self._save_tags(self.object, tag_names)
        return response
    
    def _save_tags(self, post, tag_names):
        post.tags.clear()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_created(name=name)
            post.tags.add(tag)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allow authors to edit their own posts."""
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

   
    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill tags_input from existing tags
        initial['tags_input'] = ', '.join(self.object.tags.values_list('name', flat=True))
        return initial

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        tag_names = form.cleaned_data.get('tags_input', [])
        self._save_tags(self.object, tag_names)
        return response

    def _save_tags(self, post, tag_names):
        post.tags.clear()
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            post.tags.add(tag)

class PostByTagListView(ListView):
    template_name = "blog/tag_post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['tag_slug']).distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag_slug'] = self.kwargs['tag_slug']
        return ctx


class SearchResultsView(ListView):
    template_name = "blog/search_results.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return Post.objects.none()
        # Match title, content, or tag name
        return (
            Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            )
            .distinct()
            .select_related('author')
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '').strip()
        return ctx    
                
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allow authors to delete their own posts."""
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        return self.get_object().author == self.request.user
