import uuid

from django.db import models


class Template(models.Model):
    template_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    list = models.OneToOneField(
        'List',
        on_delete=models.CASCADE,
        related_name='list_template'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
