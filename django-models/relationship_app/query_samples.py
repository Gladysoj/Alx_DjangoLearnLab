from relationship_app.models import Author, Book, Library, Librarian


orwell = Author.objects.get(name="George Orwell")
books_by_orwell = Book.objects.filter(author=orwell)
print("Books by George Orwell:", books_by_orwell)

central_library = Library.objects.get(name="Central Library")
books_in_library = central_library.books.all()
print("Books in Central Library:", books_in_library)

librarian = Librarian.objects.get(library=central_library)
print("Librarian for Central Library:", librarian.name)
