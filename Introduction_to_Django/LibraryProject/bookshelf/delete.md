# Update Book Title

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.title = "Nineteen Eighty-Four"
book.delete()
book.objects.all()

```
