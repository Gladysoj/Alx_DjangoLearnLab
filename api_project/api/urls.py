from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'book_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),

    path('', include(router.urls)),
]