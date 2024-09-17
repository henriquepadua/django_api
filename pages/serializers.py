from rest_framework import serializers
from pages.models import Author, Book, BookInstance, Genre

class BookInstanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = BookInstance
    fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
  bookinstance_set = BookInstanceSerializer(many=True)
  class Meta:
    model = Book
    fields = '__all__'
              # ,'genre','instance']
    
class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Author
    fields = '__all__'
        
class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'  