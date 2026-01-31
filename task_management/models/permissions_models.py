from django.db import models


class PermissionType(models.TextChoices):
    FULL_EDIT = "full_edit", "Full Edit"
    VIEW = "view", "View"
    COMMENT = "comment", "Comment"

class SpacePermission(models.Model):
    space = models.ForeignKey(
        "Space",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.DO_NOTHING,
        related_name='space_permissions'
    )
    permission_type = models.CharField(max_length=20, choices=PermissionType.choices)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='space_permissions_added'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username


class FolderPermission(models.Model):
    folder = models.ForeignKey(
        "Folder",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.DO_NOTHING,
        related_name='folder_permissions'
    )
    permission_type = models.CharField(max_length=20, choices=PermissionType.choices)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='folder_permissions_added'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.user.username


class ListPermission(models.Model):
    list = models.ForeignKey(
        "List",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.DO_NOTHING,
        related_name='list_permissions'
    )
    permission_type = models.CharField(max_length=20, choices=PermissionType.choices)
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