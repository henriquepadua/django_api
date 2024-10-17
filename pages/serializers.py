from datetime import date
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

  #book = serializers.StringRelatedField()#serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = '__all__'

    # Validação para a data de devolução
    def validate_due_back(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("A data de devolução não pode ser anterior à data atual.")
        return value

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
      book_instances = BookInstance.objects.filter(book=obj)

      # Retorna apenas os IDs das instâncias
      return BookInstanceSerializer(book_instances, many=True).data
  
  def validate_isbn(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("O ISBN deve conter apenas números.")
        if len(value) != 13:
            raise serializers.ValidationError("O ISBN deve conter exatamente 13 caracteres.")
        return value
        
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
        
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    # Validação para o primeiro nome
    def validate_first_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("O primeiro nome deve conter pelo menos 2 caracteres.")
        return value

    # Validação para o último nome
    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("O sobrenome deve conter pelo menos 2 caracteres.")
        return value

    # Validação para garantir que a data de falecimento não seja anterior à data de nascimento
    def validate(self, data):
        if data['date_of_death'] and data['date_of_birth'] and data['date_of_death'] < data['date_of_birth']:
            raise serializers.ValidationError("A data de falecimento não pode ser anterior à data de nascimento.")
        return data
        
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
      model = Genre
      fields = '__all__'

    # Validação para garantir que o nome tenha pelo menos 3 caracteres
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("O nome do gênero deve ter pelo menos 3 caracteres.")
        return value