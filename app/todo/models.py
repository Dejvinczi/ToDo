from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import BaseUserManager


class TaskManager(BaseUserManager):
    """Task model manager."""

    def get_owner_tasks(self, owner):
        return self.filter(owner=owner)

    def get_today_tasks(self):
        """Retrieve archived tasks. """
        now = timezone.now().date()
        return self.filter(event_date__date=now, is_archived=True)

    def get_archived_tasks(self):
        """Retrieve archived tasks. """
        return self.filter(is_archived=True)

    def get_unarchived_tasks(self):
        """Retrieve unarchived tasks"""
        return self.filter(is_archived=False)

    def get_high_priority_tasks(self):
        """Retrieve tasks with high priority."""
        return self.filter(priority=Task.HIGH_PRIORITY)

    def get_medium_priority_tasks(self):
        """Retrieve tasks with medium priority."""
        return self.filter(priority=Task.MEDIUM_PRIORITY)

    def get_low_priority_tasks(self):
        """Retrieve tasks with low priority."""
        return self.filter(priority=Task.LOW_PRIORITY)

    def get_no_priority_tasks(self):
        """Retrieve tasks with no priority."""
        return self.filter(priority=Task.NO_PRIORITY)

    def get_overdue_tasks(self):
        """Retrieve tasks that are overdue."""
        now = timezone.now()
        return self.filter(event_date__lt=now, is_archived=False)

    def get_tasks_by_tags(self, tags):
        """Retrieve tasks filtered by a specific tags."""
        return self.filter(tags__name__in=tags, is_archived=False)

    def get_recently_updated_tasks(self, days=7):
        """Retrieve tasks updated within the last 'days'."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return self.filter(updated_date__gte=cutoff_date, is_archived=False)


class TagManager(BaseUserManager):
    """Tag model manager."""

    def get_owner_tags(self, owner):
        return self.filter(owner=owner)


class Task(models.Model):
    """Application task model."""
    HIGH_PRIORITY = 3
    MEDIUM_PRIORITY = 2
    LOW_PRIORITY = 1
    NO_PRIORITY = 0

    PRIORITY_CHOICES = (
        (HIGH_PRIORITY, 'High'),
        (MEDIUM_PRIORITY, 'Medium'),
        (LOW_PRIORITY, 'Low'),
        (NO_PRIORITY, '-'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='tasks')
    label = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    event_date = models.DateTimeField(null=True)
    is_archived = models.BooleanField(default=False)
    archived_date = models.DateTimeField(null=True, blank=True)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES)
    tags = models.ManyToManyField('todo.Tag', related_name='tasks')

    objects = TaskManager()

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.label

    def archive(self):
        """Task class method to archive task."""
        if self.is_archived:
            raise ValueError(_("Task is already archived."))

        self.is_archived = True
        self.archived_date = timezone.now()
        self.save()

    def unarchive(self):
        """Task class method to unarchive task."""
        if not self.is_archived:
            raise ValueError(_("Task is not archived."))

        self.is_archived = False
        self.archived_date = None
        self.save()


class Tag(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=15)

    objects = TagManager()

    class Meta:
        unique_together = ('owner', 'name')

    def __str__(self):
        return self.name
