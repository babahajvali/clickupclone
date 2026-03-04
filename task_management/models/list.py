import uuid

from django.db import models

from task_management.exceptions.enums import ListEntityType


class List(models.Model):
    list_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    entity_type = models.CharField(
        max_length=255, choices=ListEntityType.get_list_of_tuples())
    entity_id = models.CharField(max_length=150)
    order = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_lists'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["entity_type"]),
            models.Index(fields=["entity_id"]),
            models.Index(fields=["entity_type", "entity_id"]),
        ]

    def __str__(self):
        return self.name
