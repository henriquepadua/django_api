# pages/urls.py
from django.db import router
from django.urls import include, path
from pages import views
from rest_framework.routers import DefaultRouter
from pages.views import AuthorViewSet, BookInstanceViewSet, BookViewSet, CustomTokenObtainPairView, GenreViewSet, LoanedBooksByUserListViewSet, MyObtainTokenPairView

from rest_framework import routers, serializers, viewsets

from pages.views import UserViewSet

# Routers provide a way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

app_name = 'api'
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)

router = DefaultRouter(trailing_slash=False)
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'genre', GenreViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'bookinstance', BookInstanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
