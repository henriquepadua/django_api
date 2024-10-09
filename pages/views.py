# from django.shortcuts import render
# # Create your views here.
from argparse import Action
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime
from pages.models import Author, Genre
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from urllib import request
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from pages.models import Book, Author, BookInstance
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from pages.serializers import AuthorSerializer, BookInstanceSerializer, BookSerializer, GenreSerializer
from rest_framework import viewsets, permissions,mixins
from django.contrib.auth import authenticate, login
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class BookViewSet(viewsets.ModelViewSet,mixins.CreateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    #permission_classes = [IsAuthenticated]  # Garante que apenas usuários autenticados possam acessar

class UserViewSet(viewsets.ModelViewSet,mixins.CreateModelMixin):
    serializer_class = UserSerializer

    def get_queryset(self):
        # Exclui o usuário logado do queryset
        return User.objects.exclude(id=self.request.user.id)

class AuthorViewSet(viewsets.ModelViewSet):
  queryset = Author.objects.all()
  serializer_class = AuthorSerializer
  permission_classes = [permissions.IsAuthenticated]
  
class BookInstanceViewSet(viewsets.ModelViewSet):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer
    permission_classes = [IsAuthenticated]  # Garante que apenas usuários autenticados possam acessar
    
    def list(self, request):
        queryset = BookInstance.objects.filter(borrower=self.request.user).order_by('due_back')
        serializer = BookInstanceSerializer(queryset, many=True)
        return Response(serializer.data)
    
class GenreViewSet(viewsets.ModelViewSet):
  queryset = Genre.objects.all()
  serializer_class = GenreSerializer
  permission_classes = [permissions.IsAuthenticated]      

class LoanedBooksByUserListViewSet(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='pages/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = BookInstance.objects.filter(borrower=self.request.user).order_by('due_back')
        #print(user)
        return queryset

@permission_required('login')
def Livros(request):
    books = Book.objects.all()

    context = {
        'books': books
    }
    
    return render(request, 'pages/books.html', context)    
    
class AuthorCreateView(LoginRequiredMixin,CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

    def get_success_url(self):
        return reverse('author_detail', kwargs={'pk': self.object.pk})

class AuthorDetailView(LoginRequiredMixin,generic.DetailView):
    model = Author
    paginate_by = 10
    def author_detail_view(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request, 'pages/author_detail.html', context={'author': author})

#@permission_required('catalog.can_mark_returned')
class AuthorUpdateView(LoginRequiredMixin,UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    
    def get_success_url(self):
        return reverse('author_detail', kwargs={'pk': self.object.pk})
    
class AuthorDeleteView(LoginRequiredMixin,DeleteView):
    permission_required = 'author_delete'
    model = Author
    success_url = reverse_lazy('authors')
    error_url = reverse_lazy('books')
    success_message = model._meta.verbose_name + " deleted successfully."
    
    def post(self, request, pk, *args, **kwargs):
        try:
            object = self.get_object()
            object.delete()
            print(object)
            return HttpResponseRedirect(reverse("authors"))
        except Exception as e:
            return render(request,"pages/author_error.html")
        
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'pages/book_renew_librarian.html', context)

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(('Invalid date - renewal in past'))

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='pages/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        user = BookInstance.objects.filter(borrower=self.request.user).order_by('due_back')
        #print(user)
        return user

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    #sessions
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # The 'all()' is implied by default.
    num_authors = Author.objects.all().count

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits':num_visits
    }
    
    return render(request, 'pages/index.html', context=context)

def catalog(request):
    return render(request,"pages/catalog.html",{})

def BookListView(request):
    books = Book.objects.all()
    
    context = {
        'books': books
    }
    
    return render(request, 'pages/books.html', context)
    
def AuthorListView(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    
    return render(request, 'pages/authors.html', context)

class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book
    paginate_by = 10
        
    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'pages/book_detail.html', context={'book': book})
    
class BookCreateView(LoginRequiredMixin,CreateView,mixins.CreateModelMixin):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre']

    def form_valid(self, form):
        book = form.save(commit=False)
        genres = form.cleaned_data['genre']
        book.genre.set(genres)  # Use set to update the many-to-many field
        return super().form_valid(form)
    # model = Book
    # fields = '__all__'
    # initial = {'date_of_death': '05/01/2018'}
    
    # def get_success_url(self):
    #     return reverse('book-detail', kwargs={'pk': self.object.pk})

class BookUpdateView(LoginRequiredMixin,UpdateView):
    model = Book
    fields = ['title', 'author', 'summary','isbn','genre']
    
    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.pk})
    
class BookDeleteView(LoginRequiredMixin,DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    
class BookInstanceDetailView(LoginRequiredMixin,generic.DetailView):
    model = BookInstance
    paginate_by = 10
    def bookinstance_detail_view(request, primary_key):
        bookinstance = get_object_or_404(BookInstance, pk=primary_key)
        return render(request, 'pages/bookinstance_detail.html', context={'bookinstance': bookinstance})    
    
class BookInstanceCreateView(LoginRequiredMixin,CreateView):
    model = BookInstance
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

    def get_success_url(self):
        return reverse('bookinstance_detail', kwargs={'pk': self.object.id})

class BookInstanceUpdateView(LoginRequiredMixin,UpdateView):
    model = BookInstance
    fields = '__all__'
    
    def get_success_url(self):
        return reverse('bookinstance_detail', kwargs={'pk': self.object.id})
    
class BookInstanceDeleteView(LoginRequiredMixin,DeleteView):
    model = BookInstance
    success_url = reverse_lazy('books')
    
    # def deletarAuthor(request,exception):
    #     if exception:
    #         return redirect('your-custom-error-view-name', error='error messsage')
    #     return render(request,"pages/books.html",{})

