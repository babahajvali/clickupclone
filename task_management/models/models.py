import uuid
from django.db import models


class PermissionType(models.TextChoices):
    FULL_EDIT = "full_edit", "Full Edit"
    VIEW = "view", "View"
    COMMENT = "comment", "Comment"


class RoleType(models.TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Admin"
    MEMBER = "member", "Member"
    GUEST = "guest", "Guest"


class User(models.Model):
    class GenderType(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHERS = "OTHERS", "Others"

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_url = models.URLField(null=True, blank=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=15, choices=GenderType.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_active", "created_at"]),
        ]

    def __str__(self):
        return self.username


class Account(models.Model):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    owner = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='user_account'
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


class AccountMember(models.Model):
    account = models.ForeignKey(
        'Account',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.DO_NOTHING,
        related_name='account_member'
    )
    role = models.CharField(max_length=255, choices=RoleType.choices)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='account_members_added'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["account"]),
            models.Index(fields=["user",]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return f"{self.account.name} - {self.user.username}"


class Workspace(models.Model):
    workspace_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
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


class Space(models.Model):
    space_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    workspace = models.ForeignKey(
        'Workspace',
        on_delete=models.CASCADE,
        related_name='workspace_space'
    )
    is_active = models.BooleanField(default=True)
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
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name


class Folder(models.Model):
    folder_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    space = models.ForeignKey(
        "Space",
        on_delete=models.CASCADE,
        related_name='space_folder'
    )
    order = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='folders_created'
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
    list_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    space = models.ForeignKey(
        "Space",
        on_delete=models.CASCADE,
        related_name='space_list'
    )
    folder = models.ForeignKey(
        "Folder",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='folder_list'
    )
    order = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='lists_created'
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
            models.Index(fields=["list", "is_deleted"]),
        ]

    def __str__(self):
        return self.title


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


class Field(models.Model):
    class FieldType(models.TextChoices):
        DROPDOWN = "dropdown", "Dropdown"
        USER = "user", "User"
        TEXT = "text", "Text"
        NUMBER = "number", "Number"
        DATE = "date", "Date"
        CHECKBOX = "checkbox", "Checkbox"
        EMAIL = "email", "Email"

    field_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    field_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    description = models.TextField()
    field_type = models.CharField(max_length=50, choices=FieldType.choices)
    template = models.ForeignKey(
        'Template',
        on_delete=models.CASCADE,
        related_name='fields'
    )
    order = models.PositiveIntegerField()
    config = models.JSONField(default=dict, blank=True)
    is_required = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_fields'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['template', 'is_active']),]

    def __str__(self):
        return self.field_name


class FieldValue(models.Model):
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
        indexes = [
            models.Index(fields=['task'])]

    def __str__(self):
        return self.field.field_name


class WorkspaceMember(models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='workspace_memberships'
    )
    role = models.CharField(max_length=15, choices=RoleType.choices, default=RoleType.MEMBER)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='workspace_members_added'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username


class SpacePermission(models.Model):
    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='space_permissions'
    )
    permission_type = models.CharField(max_length=20, choices=PermissionType.choices)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        User,
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
        Folder,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='folder_permissions'
    )
    permission_type = models.CharField(max_length=20, choices=PermissionType.choices)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        User,
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
        List,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='list_permissions'
    )
    permission_type = models.CharField(max_length=20, choices=PermissionType.choices)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='list_permissions_added'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username


class PasswordResetToken(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens'
    )
    token = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'password_reset_tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"Reset token for {self.user.email} - {self.token[:10]}..."