import uuid

from django.db import models

from task_management.exceptions.enums import FieldType


class Field(models.Model):
    field_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                editable=False)
    field_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    field_type = models.CharField(max_length=50,
                                  choices=FieldType.get_list_of_tuples())
    template = models.ForeignKey(
        'Template',
        on_delete=models.CASCADE,
        related_name='fields'
    )
    order = models.PositiveIntegerField()
    config = models.JSONField(default=dict, blank=True, null=True)
    is_required = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_fields'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['templates', 'is_active']), ]

    def __str__(self):
        return self.field_name


class FieldValue(models.Model):
    field = models.ForeignKey(
        'Field',
        on_delete=models.CASCADE,
        related_name='field_values'
    )
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='task_field_values'
    )
    value = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='field_values_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['tasks'])]

    def __str__(self):
        return self.field.field_name
