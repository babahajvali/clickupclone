from django.db import models

from task_management.exceptions.enums import ViewType


class ListView(models.Model):
    list = models.ForeignKey(
        'List',
        on_delete=models.CASCADE,
        related_name='list_views'
    )
    view_name = models.CharField(max_length=255, null=True, blank=True)
    view_type = models.CharField(
        max_length=50, choices=ViewType.get_list_of_tuples())
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='list_views_applied'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.list.name} - {self.view_type}"
