# pages/urls.py
from django.db import router
from django.urls import include, path
from pages import views
from rest_framework.routers import DefaultRouter
from pages.views import AuthorViewSet, BookInstanceViewSet, BookViewSet, GenreViewSet, LoanedBooksByUserListViewSet

# app_name = 'pages/api'

# router = DefaultRouter(trailing_slash=False)
# router.register(r'books', BookViewSet)
# router.register(r'genre', GenreViewSet)
# router.register(r'author', AuthorViewSet)
# router.register(r'bookinstance', BookInstanceViewSet)
#router.register(r'my-borrowed', LoanedBooksByUserListViewSet)
    # path('api/', include(router.urls)),

urlpatterns = [
    # Inclui as rotas da API registradas no router    
    # Rotas tradicionais baseadas em views genéricas do Django
    path('', views.index,name="index"),
    path('catalog/', views.catalog, name='catalog'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create/', views.BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('authors/', views.AuthorListView, name='authors'),
    path('books/', views.BookListView, name='books'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    path('bookinstance/create/', views.BookInstanceCreateView.as_view(), name='bookinstance_create'),
    path('bookinstance/<uuid:pk>/update/', views.BookInstanceUpdateView.as_view(), name='bookinstance_update'),
    path('bookinstance/<uuid:pk>/delete/', views.BookInstanceDeleteView.as_view(), name='bookinstance_delete'),
    path('bookinstance/<uuid:pk>', views.BookInstanceDetailView.as_view(), name='bookinstance_detail'),
    path('consumindo_books/',views.BooksPage.as_view(),name='consumindo_book'),
    path('consumindo_authors/',views.AuthorsPage.as_view(),name='consumindo_author')
]               

# urlpatterns = [
#     path("catalog/",views.catalog,name=''),
#     # path('books', views.Livros, name='books'),
#     path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
#     path('book/create/', views.BookCreateView.as_view(), name='book_create'),
#     path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
#     path('book/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
#     path('authors/', views.AuthorListView, name='authors'),
#     path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
#     path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
#     path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
#     path('author/create/', views.AuthorCreateView.as_view(), name='author_create'),
#     path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author_update'),
#     path('author/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
#     path('bookinstance/create/', views.BookInstanceCreateView.as_view(), name='bookinstance_create'),
#     path('bookinstance/<uuid:pk>/update/', views.BookInstanceUpdateView.as_view(), name='bookinstance_update'),
#     path('bookinstance/<uuid:pk>/delete/', views.BookInstanceDeleteView.as_view(), name='bookinstance_delete'),
#     path('bookinstance/<uuid:pk>', views.BookInstanceDetailView.as_view(), name='bookinstance_detail'),
# ]