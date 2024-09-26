from rest_framework import serializers
from pages.models import Author, Book, BookInstance, Genre

class BookInstanceSerializer(serializers.ModelSerializer):
  class Meta:
    model = BookInstance
    fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
  bookinstance_set = BookInstanceSerializer(many=True,required=False)
  class Meta:
    model = Book
    fields = '__all__'
              # ,'genre','instance']
  def create(self, validated_data):
    # Extrai o conjunto de instâncias de livro
    bookinstance_data = validated_data.pop('bookinstance_set')

    # Cria a instância do livro
    book = Book.objects.create(**validated_data)

    # Cria as instâncias de livro associadas
    for book_instance in bookinstance_data:
        BookInstance.objects.create(book=book, **book_instance)

    return book            
    
class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Author
    fields = '__all__'
        
class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'  