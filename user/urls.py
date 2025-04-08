from django.urls import path
from .views import *

urlpatterns = [
    path('create_superuser', create_superuser),
    path('login', login),
]