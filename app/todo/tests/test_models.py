"""
Todo models tests.
"""
import pytest

from core.tests.factories.user_factory import UserFactory

from .. import models
from .factories import (
    tag_factory,
    task_factory,
)


@pytest.mark.django_db
class TestTagModel:
    """Tag model tests."""

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = UserFactory()
        tag_dict = {'owner': user, 'name': 'Tag1'}
        tag = tag_factory.TagFactory(**tag_dict)

        assert tag.name == tag_dict['name']
        assert tag.owner == tag_dict['owner']
        assert tag.tasks.count() == 0


@pytest.mark.django_db
class TestTaskModel:
    """Task model tests."""

    def test_create_task(self):
        """Create new task test."""
        user = UserFactory()
        task_dict = {'label': 'TestTask1', 'priority': 1, 'owner': user}
        task = task_factory.TaskFactory(**task_dict)

        assert models.Task.objects.count() == 1
        assert task.label == task_dict['label']
        assert task.priority == task_dict['priority']
        assert task.owner == task_dict['owner']
        assert not task.is_archived
        assert task.tags.count() == 0

    def test_archive_task(self):
        """Archive task test."""
        task = task_factory.TaskFactory(is_archived=False, archived_date=None)

        assert not task.is_archived
        assert task.archived_date is None

        task.archive()

        assert task.is_archived
        assert task.archived_date is not None
