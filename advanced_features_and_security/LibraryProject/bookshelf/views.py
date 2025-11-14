from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from .forms import ExampleForm
from django import forms
from .models import Book
from .forms import SearchForm

def create_book(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})

class SearchForm(forms.Form):
    title = forms.CharField(max_length=200)

def search_books(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        title = form.cleaned_data["title"]
        books = Book.objects.filter(title__icontains=title)
        return render(request, "bookshelf/book_list.html", {"books": books, "form": form})
    else:
        return render(request, "bookshelf/book_list.html", {"form": form})

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})

@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    # logic for creating a book
    pass

@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # logic for editing a book
    pass

@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # logic for deleting a book
    pass
