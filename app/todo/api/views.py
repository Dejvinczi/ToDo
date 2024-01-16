"""
Todo API views.
"""
from django.utils.translation import gettext as _
from rest_framework import (
    viewsets,
    status,
    exceptions
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from todo import models
from . import serializers


class TagViewSet(viewsets.ModelViewSet):
    """Manage tag API."""
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve tasks for authenticated user."""
        self.queryset = models.Tag.objects.get_owner_tags(self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        """Create a new tag."""
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    """Manage tasks API."""
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve tasks for authenticated user."""
        self.queryset = models.Task.objects.get_owner_tasks(self.request.user)
        return super().get_queryset()

    def get_serializer_class(self, *args, **kwargs):
        """Return the serializer class for request."""
        match self.action:
            case 'list' | 'todays_tasks' | 'archived_tasks':
                return serializers.TaskSerializer
            case 'archive' | 'unarchive':
                return None

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new task."""
        serializer.save(owner=self.request.user)

    @action(methods=['GET'],
            detail=False,
            url_path='today')
    def today_tasks(self, request):
        """Return today tasks."""
        queryset = models.Task.objects.get_today_tasks()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'],
            detail=False,
            url_path='archived')
    def archived_tasks(self, request):
        """Return archived tasks."""
        queryset = models.Task.objects.get_archived_tasks()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'],
            detail=True,
            url_path='archive')
    def archive(self, request, pk=None):
        """Mark task as archived."""
        task = self.get_object()

        try:
            task.archive()
        except ValueError as ve:
            raise exceptions.ValidationError({'error': str(ve)})

        return Response(
            {'message': _(f'Task "{task}" has been successfully archived.')},
            status=status.HTTP_200_OK,
        )

    @action(methods=['POST'],
            detail=True,
            url_path='unarchive')
    def unarchive(self, request, pk=None):
        """Mark task as unarchived."""
        task = self.get_object()

        try:
            task.unarchive()
        except ValueError as ve:
            raise exceptions.ValidationError({'error': str(ve)})

        return Response(
            {'message': _(f'Task "{task}" has been successfully unarchived.')},
            status=status.HTTP_200_OK,
        )
