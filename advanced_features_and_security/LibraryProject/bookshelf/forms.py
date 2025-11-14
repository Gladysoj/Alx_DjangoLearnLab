# bookshelf/forms.py
from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    """
    ExampleForm demonstrates secure form handling with CSRF protection.
    It is tied to the Book model and validates user input safely.
    """
    class Meta:
        model = Book
        fields = ["title", "author", "published_date"]

class SearchForm(forms.Form):
    title = forms.CharField(max_length=200)
