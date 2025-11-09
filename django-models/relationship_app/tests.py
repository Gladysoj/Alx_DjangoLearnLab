# relationship_app/tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Author, Book, Library, Librarian

class RelationshipAppTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Gladys")
        self.book = Book.objects.create(title="Django Deep Dive", author=self.author)
        self.library = Library.objects.create(name="Central Library")
        self.library.books.add(self.book)
        self.librarian = Librarian.objects.create(name="Libby", library=self.library)

    def test_books_by_author(self):
        books = Book.objects.filter(author=self.author)
        self.assertEqual(books.count(), 1)
        self.assertEqual(books.first().title, "Django Deep Dive")

    def test_library_books(self):
        books = self.library.books.all()
        self.assertIn(self.book, books)

    def test_librarian_for_library(self):
        librarian = Librarian.objects.get(library=self.library)
        self.assertEqual(librarian.name, "Libby")

    def test_list_books_view(self):
        response = self.client.get(reverse('list_books'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Deep Dive")
