"""Core serializers."""
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for obtain pair of tokens."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        return token


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, min_length=5, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        try:
            user = get_user_model().objects.create_user(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'email': 'User with this email already exist.'})

        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
