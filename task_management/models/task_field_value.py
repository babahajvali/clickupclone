from django.db import models


class TaskFieldValue(models.Model):
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
        unique_together = [("task", "field")]
        indexes = [
            models.Index(fields=['task'])]

    def __str__(self):
        return self.field.field_name
