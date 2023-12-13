"""Common setup for tests."""
import pytest


@pytest.fixture
def create_user(db, django_user_model):
    """Creating user fixture."""
    def make_user(email='tesuser@example.com', password='testuserpass', **kwargs):
        return django_user_model.objects.create_user(email, password, **kwargs)

    return make_user


@pytest.fixture
def create_superuser(db, django_user_model):
    """Creating superuser fixture."""
    def make_superuser(email='testsuperuser@example.com', password='testsuperuserpass', **kwargs):
        return django_user_model.objects.create_superuser(email, password, **kwargs)

    return make_superuser


@pytest.fixture
def auth_client(client, create_user):
    """Return auth client for tests."""
    user = create_user(
        name='auth_user',
        email='auth_user@example.com',
        password='auth_user_pass',
    )
    client.force_login(user)
    return client
