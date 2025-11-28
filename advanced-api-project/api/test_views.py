from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()

        # Create an author and some books
        self.author = Author.objects.create(name="Jane Austen")
        self.book1 = Book.objects.create(title="Pride and Prejudice", publication_year=1813, author=self.author)
        self.book2 = Book.objects.create(title="Emma", publication_year=1815, author=self.author)

    def test_list_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(f"/api/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Pride and Prejudice")

    def test_create_book_requires_authentication(self):
        # Unauthenticated request should fail
        response = self.client.post("/api/books/create/", {
            "title": "Sense and Sensibility",
            "publication_year": 1811,
            "author": self.author.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated request should succeed
        self.client.login(username="testuser", password="password123")
        response = self.client.post("/api/books/create/", {
            "title": "Sense and Sensibility",
            "publication_year": 1811,
            "author": self.author.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.put(f"/api/books/update/{self.book1.id}/", {
            "title": "Pride & Prejudice",
            "publication_year": 1813,
            "author": self.author.id
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Pride & Prejudice")

    def test_delete_book(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.delete(f"/api/books/delete/{self.book2.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_year(self):
        response = self.client.get("/api/books/?publication_year=1813")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Pride and Prejudice")

    def test_search_books_by_title(self):
        response = self.client.get("/api/books/?search=Emma")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Emma")

    def test_order_books_by_year(self):
        response = self.client.get("/api/books/?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))
