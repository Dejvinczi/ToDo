"""Task factories."""
import datetime
import factory

from factory import fuzzy

from core.tests.factories.user_factory import UserFactory

from ...models import Task


PRIORITY_IDS = [x[0] for x in Task.PRIORITY_CHOICES]


class TaskFactory(factory.django.DjangoModelFactory):
    """Factory for creating Task instances."""
    class Meta:
        model = Task

    owner = factory.SubFactory(UserFactory)
    label = factory.Sequence(lambda n: f'Task{n}')
    description = factory.Sequence(lambda n: f'Description of Task{n}')
    priority = fuzzy.FuzzyChoice(PRIORITY_IDS)


class ArchivedTaskFactory(TaskFactory):
    """Factory for creating archived Task instances."""
    is_archived = True
    archived_date = factory.LazyFunction(datetime.datetime.now)
