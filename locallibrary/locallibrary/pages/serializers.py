from rest_framework import serializers
from pages.models import Author, Book, BookInstance, Genre

class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = '__all__'
    
class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Author
    fields = '__all__'
    
    
class BookInstanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = BookInstance
    fields = '__all__'
    
class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'  