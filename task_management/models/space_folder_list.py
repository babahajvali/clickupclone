import uuid

from django.db import models


class Space(models.Model):
    space_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    workspace = models.ForeignKey(
        'Workspace',
        on_delete=models.CASCADE,
        related_name='spaces'
    )
    is_deleted = models.BooleanField(default=False)
    order = models.PositiveIntegerField()
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='spaces_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["workspace"]),
            models.Index(fields=["is_deleted"]),
        ]

    def __str__(self):
        return self.name


class Folder(models.Model):
    folder_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    space = models.ForeignKey(
        "Space",
        on_delete=models.CASCADE,
        related_name='folders'
    )
    order = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_folders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["space"]),
        ]

    def __str__(self):
        return self.name


class List(models.Model):
    list_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    space = models.ForeignKey(
        "Space",
        on_delete=models.CASCADE,
        related_name='space_lists',
        null=True, blank=True
    )
    folder = models.ForeignKey(
        "Folder",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='folder_lists'
    )
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
            models.Index(fields=["space"]),
            models.Index(fields=["folder"]),
        ]

    def __str__(self):
        return self.name
