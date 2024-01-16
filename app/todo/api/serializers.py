"""
Todo API serializers.
"""
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from todo.models import (
    Task,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Tag model serializer."""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a new tag."""
        owner = self.context['request'].user
        tag = Tag.objects.create(owner=owner, **validated_data)
        # raise serializers.ValidationError(
        #     _('Tag with this name already exists.'))
        return tag


class TaskSerializer(serializers.ModelSerializer):
    """Task model serializer."""
    priority = serializers.ChoiceField(choices=Task.PRIORITY_CHOICES)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'label', 'event_date', 'priority', 'tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, task):
        """Handle getting or creating tags as needed."""
        owner = task.owner
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(owner=owner, **tag)
            task.tags.add(tag_obj)

    def create(self, validated_data):
        """Create a task."""
        tags = validated_data.pop('tags', [])
        task = super().create(validated_data)
        self._get_or_create_tags(tags, task)

        return task

    def update(self, instance, validated_data):
        """Update a task."""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        return super().update(instance, validated_data)


class TaskDetailSerializer(TaskSerializer):
    """Task model detail serializer."""

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + [
            'description', 'created_date', 'updated_date',
            'is_archived', 'archived_date'
        ]
        read_only_fields = TaskSerializer.Meta.read_only_fields + [
            'created_date', 'updated_date', 'is_archived', 'archived_date'
        ]
