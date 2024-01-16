"""Tag factories."""
import factory

from core.tests.factories.user_factory import UserFactory

from todo.models import Tag


class TagFactory(factory.django.DjangoModelFactory):
    """Tag model factory."""
    name = factory.Faker('word')
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Tag
