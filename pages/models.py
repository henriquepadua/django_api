import uuid
from django.db import models
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name
    
    def clean(self):
        # Exemplo de validação customizada para o campo "name"
        if len(self.name) < 3:
            raise ValidationError('O nome do gênero deve ter pelo menos 3 caracteres.')
    
def validate_isbn(value):
    if not value.isdigit():
        raise ValidationError('O ISBN deve conter apenas números.')
    if len(value) != 13:
        raise ValidationError('O ISBN deve conter exatamente 13 dígitos.')
    
class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13,validators=[MinLengthValidator(13)], help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])       

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:2])
    display_genre.short_description = 'Genre'
    

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this book')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    def clean(self):
        # Validação para data de devolução
        if self.due_back and self.due_back < date.today():
            raise ValidationError('A data de devolução não pode ser anterior à data de hoje.')
        
        # Validação para o status do livro
        if not self.status in dict(self.LOAN_STATUS):
            raise ValidationError('Status do livro inválido.')
        
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def clean(self):
        # Validação para primeiro e último nome
        if len(self.first_name) < 2:
            raise ValidationError('O primeiro nome deve ter pelo menos 2 caracteres.')
        if len(self.last_name) < 2:
            raise ValidationError('O sobrenome deve ter pelo menos 2 caracteres.')

        # Validação para garantir que a data de falecimento não seja anterior à data de nascimento
        if self.date_of_death and self.date_of_birth and self.date_of_death < self.date_of_birth:
            raise ValidationError('A data de falecimento não pode ser anterior à data de nascimento.')