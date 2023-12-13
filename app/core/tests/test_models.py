"""
Core models tests.
"""
import pytest

from core.models import User
from .factories.user_factory import (
    UserFactory,
    SuperuserFactory,
)


@pytest.mark.django_db
class TestUser:
    """User model tests."""

    def test_create_user(self):
        """Creation user instance test."""
        email = 'user@example.com'
        password = 'userpass'
        user = User.objects.create_user(email=email, password=password)

        # Verify user properties
        assert user.email == email
        assert user.check_password(password)
        assert not user.is_superuser
        assert not user.is_staff

    def test_create_superuser(self):
        """"Creation superuser instance test."""
        email = 'admin@example.com'
        password = 'adminpass'
        superuser = User.objects.create_superuser(
            email=email, password=password)

        # Verify superuser properties
        assert superuser.email == email
        assert superuser.check_password(password)
        assert superuser.is_superuser
        assert superuser.is_staff

    def test_update_user(self):
        """Updating user instance test."""
        email = 'user@example.com'
        user = UserFactory(email=email)
        db_users = User.objects.filter(is_superuser=False)

        # Verify creating user in db
        assert db_users.count() == 1
        assert db_users.first() == user

        db_user = db_users.first()

        # Verify email
        assert db_user.email == email

        new_name = 'new_user'
        new_email = 'new_user@example.com'
        new_password = 'new_password'

        user.name = new_name
        user.email = new_email
        user.set_password(new_password)
        user.save()
        db_user.refresh_from_db()

        # Verify new properties
        assert db_user.name == new_name
        assert db_user.email == new_email
        assert db_user.check_password(new_password)

    def test_update_superuser(self):
        """Updating superuser instance test."""
        email = 'admin@example.com'
        superuser = SuperuserFactory(email=email)
        db_superusers = User.objects.filter(is_superuser=True)

        # Verify creating superuser in db
        assert db_superusers.count() == 1
        assert db_superusers.first() == superuser

        db_superuser = db_superusers.first()

        # Verify email
        assert db_superuser.email == email

        new_name = 'new_admin'
        new_email = 'new_admin@example.com'
        new_password = 'new_password'

        superuser.name = new_name
        superuser.email = new_email
        superuser.set_password(new_password)
        superuser.save()
        db_superuser.refresh_from_db()

        # Verify new properties
        assert db_superuser.name == new_name
        assert db_superuser.email == new_email
        assert db_superuser.check_password(new_password)

    def test_delete_user(self):
        """Deleting user instance test."""
        user = UserFactory()
        db_users = User.objects.filter(is_superuser=False)

        # Verify creating user in db
        assert db_users.count() == 1
        assert db_users.first() == user

        user.delete()

        # Verify deleting user
        assert db_users.count() == 0

    def test_delete_superuser(self):
        """Deleting superuser instance test."""
        superuser = SuperuserFactory()
        db_superusers = User.objects.filter(is_superuser=True)

        # Verify creating superuser in db
        assert db_superusers.count() == 1
        assert db_superusers.first() == superuser

        superuser.delete()

        # Verify deleting superuser
        assert db_superusers.count() == 0
