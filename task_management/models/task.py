import uuid

from django.db import models


class Task(models.Model):
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    list = models.ForeignKey(
        'List',
        on_delete=models.CASCADE,
        related_name='list_tasks'
    )
    order = models.PositiveIntegerField()
    is_deleted = models.BooleanField(default=False, db_index=True)
    created_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tasks_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["lists", "is_deleted"]),
        ]

    def __str__(self):
        return self.title

class TaskAssignee(models.Model):
    assign_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        related_name='task_assignees'
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.DO_NOTHING,
        related_name='assigned_tasks'
    )
    is_active = models.BooleanField(default=True)
    assigned_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tasks_assigned_by_me'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.task.title}"