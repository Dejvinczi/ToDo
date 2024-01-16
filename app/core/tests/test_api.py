"""
Core views tests.
"""
import pytest

from django.urls import reverse
from rest_framework import status


REGISTER_URL = reverse('register')
TOKEN_URL = reverse('get_token')
TOKEN_REFRESH_URL = reverse('refresh_token')
ME_URL = reverse('me')


@pytest.mark.django_db
class TestPublicUserAPI:
    """Test the public features of the user API."""

    def test_register_new_user(self, client, django_user_model):
        """Test register a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = client.post(REGISTER_URL, payload)

        # Check response status and data
        assert res.status_code == status.HTTP_201_CREATED
        assert 'password' not in res.data

        user = django_user_model.objects.get(email=payload['email'])

        # Check created user properly password
        assert user.check_password(payload['password'])

    def test_user_with_email_exists_error(self, client, create_user):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        create_user(**payload)
        res = client.post(REGISTER_URL, payload)

        # Check response status
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_too_short_error(self, client):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }

        res = client.post(REGISTER_URL, payload)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_token_for_user(self, client, create_user):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test name',
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = client.post(TOKEN_URL, payload)

        assert res.status_code == status.HTTP_200_OK
        assert 'access' in res.data
        assert 'refresh' in res.data

    def test_create_token_bad_credentials(self, client, create_user):
        """Test return error if credentials invalid."""
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = client.post(TOKEN_URL, payload)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'access' not in res.data
        assert 'refresh' not in res.data

    def test_create_token_blank_password(self, client):
        """Test posting a blank password return an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        res = client.post(TOKEN_URL, payload)

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'access' not in res.data
        assert 'refresh' not in res.data

    def test_retrive_user_unauthorized(self, client):
        """Test authentication is required for users."""
        res = client.get(ME_URL)

        assert res.status_code == status.HTTP_401_UNAUTHORIZED


class PrivateUserApiTests:
    """Test API requests that require authentication."""

    def test_retrive_profile_success(self, client, create_user):
        """Test retrieving profile for logged is user."""
        user = create_user()
        client.force_login(user)

        res = client.get(ME_URL)

        assert res.status_code == status.HTTP_200_OK
        assert res.data == {
            'name': self.user.name,
            'email': self.user.email,
        }

    def test_post_me_not_allowed(self, auth_client):
        """Test POST is not allowed for the me endpoint."""
        res = auth_client.post(ME_URL, {})

        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update_user_profile(self, client, create_user):
        """Test updating the user profile for the authenticated user."""
        user = create_user()
        client.force_login(user)
        payload = {'name': 'Updated name', 'password': 'newppassword123'}

        res = client.patch(ME_URL, payload)
        user.refresh_from_db()

        assert res.status_code == status.HTTP_200_OK
        assert user.name == payload['name']
        assert user.check_password(payload['password'])
