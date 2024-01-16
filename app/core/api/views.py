"""
Core API views.
"""
from rest_framework import (
    generics,
    permissions,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
)


class CreateUserAPIView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenPairAPIView(TokenObtainPairView):
    """Create a new auth token for user."""
    serializer_class = CustomTokenObtainPairSerializer


class RefreshTokenAPIView(TokenRefreshView):
    """Refresh user auth token."""
    serializer_class = CustomTokenObtainPairSerializer


class ManageUserAPIView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
