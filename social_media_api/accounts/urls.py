from django.urls import path, include
from .views import RegisterView, LoginView, ProfileView
from .views import FollowUserView, UnfollowUserView, MeView
from .views import RegisterSerializer, LoginSerializer


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('api/accounts/', include('accounts.urls')),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('me/', MeView.as_view(), name='me'),

     path('feed/', FeedView.as_view(), name='feed'),
]

urlpatterns += router.urls