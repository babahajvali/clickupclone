from django.contrib import admin
from task_management.models import (
    User, Account, Workspace, WorkspaceMember,
    Space, SpacePermission, Folder, FolderPermission,
    List, ListPermission, Task, TaskAssignee,
    Template, Field, FieldValue, View, ListView
)
from task_management.models.user import PasswordResetToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id', 'email', 'full_name', 'gender',
                    'is_active', 'created_at')
    list_filter = ('is_active', 'gender', 'created_at')
    search_fields = ('username', 'email', 'full_name', 'phone_number')
    readonly_fields = ('user_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_id', 'owner', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('account_id', 'created_at', 'updated_at')
    raw_id_fields = ('owner',)



@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'workspace_id', 'accounts', 'created_by',
                    'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('workspace_id', 'created_at', 'updated_at')
    raw_id_fields = ('accounts', 'created_by')


@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
    list_display = ('workspaces', "pk", 'user', 'role', 'is_active', 'added_by',
                    'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('workspace__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('workspaces', 'user', 'added_by')


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'space_id', 'workspaces', 'order', 'is_active',
                    'is_private',
                    'created_by', 'created_at')
    list_filter = ('is_active', 'is_private', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('space_id', 'created_at', 'updated_at')
    raw_id_fields = ('workspaces', 'created_by')
    ordering = ('workspaces', 'order')


@admin.register(SpacePermission)
class SpacePermissionAdmin(admin.ModelAdmin):
    list_display = ('spaces', 'user', 'permission_type', 'is_active',
                    'added_by', 'created_at')
    list_filter = ('permission_type', 'is_active', 'created_at')
    search_fields = ('space__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('spaces', 'user', 'added_by')


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'folder_id', 'spaces', 'order', 'is_active',
                    'is_private',
                    'created_by', 'created_at')
    list_filter = ('is_active', 'is_private', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('folder_id', 'created_at', 'updated_at')
    raw_id_fields = ('spaces', 'created_by')
    ordering = ('spaces', 'order')


@admin.register(FolderPermission)
class FolderPermissionAdmin(admin.ModelAdmin):
    list_display = ('folder', 'user', 'permission_type', 'is_active',
                    'added_by', 'created_at')
    list_filter = ('permission_type', 'is_active', 'created_at')
    search_fields = ('folder__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('folder', 'user', 'added_by')


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'list_id', 'spaces', 'folder', 'order', 'is_active',
                    'is_private', 'created_by', 'created_at')
    list_filter = ('is_active', 'is_private', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('list_id', 'created_at', 'updated_at')
    raw_id_fields = ('spaces', 'folder', 'created_by')
    ordering = ('spaces', 'order')


@admin.register(ListPermission)
class ListPermissionAdmin(admin.ModelAdmin):
    list_display = ('lists', 'user','id', 'permission_type', 'is_active', 'added_by',
                    'created_at')
    list_filter = ('permission_type', 'is_active', 'created_at')
    search_fields = ('list__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('lists', 'user', 'added_by')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_id', 'lists', 'order', 'is_deleted',
                    'created_by',
                    'created_at')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('task_id', 'created_at', 'updated_at')
    raw_id_fields = ('lists', 'created_by')
    ordering = ('lists', 'order')


@admin.register(TaskAssignee)
class TaskAssigneeAdmin(admin.ModelAdmin):
    list_display = ('tasks', "assign_id", 'user', 'is_active', 'assigned_by',
                    'assigned_at')
    list_filter = ('is_active', 'assigned_at')
    search_fields = ('task__title', 'user__username')
    readonly_fields = ('assign_id', 'assigned_at')
    raw_id_fields = ('tasks', 'user', 'assigned_by')


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_id', 'lists', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('template_id', 'created_at', 'updated_at')
    raw_id_fields = ('lists',)


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'field_id', 'field_type', "is_active",
                    'templates', 'order',
                    'is_required', 'created_by', 'created_at')
    list_filter = ('field_type', 'is_required', 'created_at')
    search_fields = ('field_name', 'description')
    readonly_fields = ('field_id', 'created_at', 'updated_at')
    raw_id_fields = ('templates', 'created_by')
    ordering = ('templates', 'order')


@admin.register(FieldValue)
class FieldValueAdmin(admin.ModelAdmin):
    list_display = ('fields', 'tasks', 'value', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('field__field_name', 'task__title')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('fields', 'tasks', 'created_by')


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('name', 'view_id', 'view_type', 'created_by', 'created_at')
    list_filter = ('view_type', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('view_id', 'created_at', 'updated_at')
    raw_id_fields = ('created_by',)


@admin.register(ListView)
class ListViewAdmin(admin.ModelAdmin):
    list_display = ('lists', 'views', 'is_active', 'applied_by', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('list__name', 'view__name')
    readonly_fields = ('created_at',)
    raw_id_fields = ('lists', 'views', 'applied_by')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_preview', 'created_at', 'id', 'expires_at',
                    'is_used')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__email', 'user__username', 'token')
    readonly_fields = ('token', 'created_at')

    def token_preview(self, obj):
        return f"{obj.token[:20]}..."

    token_preview.short_description = 'Token'
