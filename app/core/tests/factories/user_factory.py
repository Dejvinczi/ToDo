"""User factories."""
import factory

from core.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """User - User model factory."""
    class Meta:
        """User model factory meta."""
        model = User

    name = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.django.Password(
        factory.Sequence(lambda n: f'user{n}_pass'))
    is_staff = False
    is_superuser = False
    is_active = True


class SuperuserFactory(UserFactory):
    """Superuser - User model factory."""
    name = factory.Sequence(lambda n: f'admin{n}')
    email = factory.Sequence(lambda n: f'admin{n}@example.com')
    password = factory.django.Password(
        factory.Sequence(lambda n: f'admin{n}_pass'))
    is_staff = True
    is_superuser = True
