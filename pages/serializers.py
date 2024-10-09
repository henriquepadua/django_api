from rest_framework import serializers
from pages.models import Author, Book, BookInstance, Genre
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class BookInstanceSerializer(serializers.ModelSerializer):
  #book = serializers.StringRelatedField()#serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
  class Meta:
    model = BookInstance
    fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
  genre = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())
  bookinstance_set = serializers.SerializerMethodField()
    
  class Meta:
      model = Book
      fields = '__all__'

  def get_bookinstance_set(self, obj):
        # Acessa o request do contexto do serializer
        request = self.context.get('request')
        
        # Filtra as instâncias de livros que pertencem ao usuário logado
        book_instances = BookInstance.objects.filter(book=obj, borrower=request.user)

        # Retorna apenas os IDs das instâncias
        return BookInstanceSerializer(book_instances, many=True).data
  # def create(self, validated_data):
  #     bookinstances_data = validated_data.pop('bookinstance_set', [])
  #     genres = validated_data.pop('genre')
  #     book = Book.objects.create(**validated_data)
  #     book.genre.set(genres)  # Use set to assign many-to-many field
  #     for bookinstance_data in bookinstances_data:
  #           BookInstance.objects.create(book=book, **bookinstance_data)
  #     return book
  # bookinstance_set = BookInstanceSerializer(many=True,required=False)
  # class Meta:
  #   model = Book
  #   fields = '__all__'
  #             # ,'genre','instance']
  # def create(self, validated_data):
  #   # Extrai o conjunto de instâncias de livro
  #   bookinstance_data = validated_data.pop('bookinstance_set')

  #   # Cria a instância do livro
  #   book = Book.objects.create(**validated_data)

  #   # Cria as instâncias de livro associadas
  #   for book_instance in bookinstance_data:
  #       BookInstance.objects.create(book=book, **book_instance)

  #   return book            

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
        
    
class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Author
    fields = '__all__'
        
class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = '__all__'  
