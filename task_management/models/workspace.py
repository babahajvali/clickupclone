import uuid

from django.db import models

from task_management.exceptions.enums import Role


class Workspace(models.Model):
    workspace_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                    editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='user_workspace'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name


class WorkspaceMember(models.Model):
    workspace = models.ForeignKey(
        "Workspace",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.DO_NOTHING,
        related_name='workspace_memberships'
    )
    role = models.CharField(max_length=15, choices=Role.get_list_of_tuples())
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='workspace_members_added'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
