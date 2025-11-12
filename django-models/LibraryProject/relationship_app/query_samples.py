from relationship_app.models import Librarian, Library

library_instance = Library.objects.get(name="Qasr Al Watan Library")  
librarian = Librarian.objects.get(library=library_instance)
print(f"Librarian for {library_instance.name}: {librarian.name}")

# 1️⃣ Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# 2️⃣ List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# 3️⃣ Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian
