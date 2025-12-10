from django.urls import path, include
from .views import LikePostView, UnlikePostView
from .views import FeedView
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from .views import NotificationListView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = router.urls

urlpatterns = [
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('posts.urls')),
    path('feed/', FeedView.as_view(), name='feed'),

    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
]
urlpatterns += router.urls