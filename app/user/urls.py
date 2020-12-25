from django.urls import path
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from .views import CreateUserAPIView, CreateTokenView, ManageUserAPIView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserAPIView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserAPIView.as_view(), name='me'),
]