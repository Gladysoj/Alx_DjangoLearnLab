from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.Modelserializer):
    """
    Serializer for the Book model.
    Includes validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

    class AuthorSerializer(serializers.ModelSerializer):
        books = BookSerializer(many=True, read_only=True)
        """
        Serializer for the Author model.
        Nests BookSerializer to show all books written by the author.
        """
        class Meta:
            model = Author
            fields = ['id', 'name', 'books']   