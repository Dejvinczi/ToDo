"""Core urls."""
from django.urls import path

from . import views

urlpatterns = [
    # Register new user in system
    path('register', views.CreateUserAPIView.as_view(), name='register'),

    # Generate token for user
    path('token', views.CreateTokenPairAPIView.as_view(), name='obtain_token'),
    path('token/refresh', views.RefreshTokenAPIView.as_view(), name='refresh_token'),

    # Authenticated user
    path('me', views.ManageUserAPIView.as_view(), name='me')

]
