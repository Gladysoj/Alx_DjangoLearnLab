# blog/urls.py
from django.urls import path
from .views import (
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    register_view, login_view, logout_view, profile_view,
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView
    
)

urlpatterns = [
    # Authentication
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),

    # Blog Posts (CRUD)
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),                # ✅ required
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),    # ✅ required
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),    # ✅ required

    path('posts/<int:post_id>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('posts/<int:post_id>/comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('posts/<int:post_id>/comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]

