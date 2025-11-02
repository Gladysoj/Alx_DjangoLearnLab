```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Ninteen Eighty-Four"
book.save()
book.title
```
