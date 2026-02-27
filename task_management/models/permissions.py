from django.db import models

from task_management.exceptions.enums import Permissions




class UserPermission(models.Model):
    entity_id = models.CharField()
    entity_type = models.CharField(max_length=20)
    user = models.ForeignKey(
        "User",
        on_delete=models.DO_NOTHING,
        related_name='list_permissions'
    )
    permission_type = models.CharField(max_length=20,
                                       choices=Permissions.get_list_of_tuples())
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='list_permissions_added'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username