# pages/urls.py
from django.db import router
from django.urls import include, path
from pages import views
from rest_framework.routers import DefaultRouter
from pages.views import AuthorViewSet, BookInstanceViewSet, BookViewSet, GenreViewSet, MyObtainTokenPairView, UserBorrowedViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet)
router.register(r'genre', GenreViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'bookinstance', BookInstanceViewSet)
router.register(r'users', UserViewSet,basename="users")
router.register(r'usersborrowed', UserBorrowedViewSet,basename="usersborrowed")

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyObtainTokenPairView.as_view(), name='login'),  # Definindo a rota para login diretamente
]
