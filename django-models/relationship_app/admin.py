from django.contrib import admin
from .models import Author, Book, Library, Librarian

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    search_fields = ('title',)
    list_filter = ('author',)


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    filter_horizontal = ('books',)  # Adds a nice interface for selecting many books


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'library')
    search_fields = ('name',)

