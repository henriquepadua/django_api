from django.db import router
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

import catalog
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include('catalog.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]