"""User factories."""
import factory

from core.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """User - User model factory."""
    class Meta:
        """User model factory meta."""
        model = User

    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.Faker('password')
    is_staff = False
    is_superuser = False
    is_active = True


class SuperuserFactory(UserFactory):
    """Superuser - User model factory."""
    is_staff = True
    is_superuser = True
