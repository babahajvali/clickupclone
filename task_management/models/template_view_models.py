import uuid

from django.db import models


class Template(models.Model):
    template_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    list = models.OneToOneField(
        'List',
        on_delete=models.CASCADE,
        related_name='list_template'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class View(models.Model):
    class ViewType(models.TextChoices):
        TABLE = "table", "Table"
        CALENDAR = "calendar", "Calendar"
        BOARD = "board", "Board"
        DASHBOARD = "dashboard", "Dashboard"
        LIST = "list", "List"
        GANTT = "gantt", "Gantt"

    view_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    view_type = models.CharField(max_length=20, choices=ViewType.choices, default=ViewType.LIST)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='views_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ListView(models.Model):
    list = models.ForeignKey(
        'List',
        on_delete=models.CASCADE,
        related_name='list_views'
    )
    view = models.ForeignKey(
        'View',
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True)
    applied_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='list_views_applied'
    )
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.list.name} - {self.view.name}"

