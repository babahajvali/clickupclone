from django.contrib import admin

from task_management.models import (
    User, Account, Workspace, WorkspaceMember,
    Space, SpacePermission, Folder, FolderPermission,
    List, ListPermission, Task, TaskAssignee,
    Template, Field, TaskFieldValue, ListView,
    Plan, Customer, Subscription, Payment,
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
    list_display = ('name', 'workspace_id', 'account', 'created_by',
                    'is_deleted', 'created_at')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('workspace_id', 'created_at', 'updated_at')
    raw_id_fields = ('account', 'created_by')


@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
    list_display = ('workspace', "pk", 'user', 'role', 'is_active', 'added_by',
                    'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('workspace__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('workspace', 'user', 'added_by')


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'space_id', 'workspace', 'order', 'is_deleted',
                    'is_private',
                    'created_by', 'created_at')
    list_filter = ('is_deleted', 'is_private', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('space_id', 'created_at', 'updated_at')
    raw_id_fields = ('workspace', 'created_by')
    ordering = ('workspace', 'order')


@admin.register(SpacePermission)
class SpacePermissionAdmin(admin.ModelAdmin):
    list_display = ('space', 'user', 'permission_type', 'is_active',
                    'added_by', 'created_at')
    list_filter = ('permission_type', 'is_active', 'created_at')
    search_fields = ('space__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('space', 'user', 'added_by')


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'folder_id', 'space', 'order', 'is_deleted',
                    'is_private',
                    'created_by', 'created_at')
    list_filter = ('is_deleted', 'is_private', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('folder_id', 'created_at', 'updated_at')
    raw_id_fields = ('space', 'created_by')
    ordering = ('space', 'order')


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
    list_display = ('name', 'list_id', 'entity_type', 'entity_id', 'order',
                    'is_deleted',
                    'is_private', 'created_by', 'created_at')
    list_filter = ('is_deleted', 'is_private', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('list_id', 'created_at', 'updated_at')
    ordering = ('entity_type', 'order')


@admin.register(ListPermission)
class ListPermissionAdmin(admin.ModelAdmin):
    list_display = ('list', 'user', 'id', 'permission_type', 'is_active',
                    'added_by',
                    'created_at')
    list_filter = ('permission_type', 'is_active', 'created_at')
    search_fields = ('list__name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('list', 'user', 'added_by')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task_id', 'list', 'order', 'is_deleted',
                    'created_by',
                    'created_at')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('task_id', 'created_at', 'updated_at')
    raw_id_fields = ('list', 'created_by')
    ordering = ('list', 'order')


@admin.register(TaskAssignee)
class TaskAssigneeAdmin(admin.ModelAdmin):
    list_display = ('task', "assign_id", 'user', 'is_active', 'assigned_by',
                    'assigned_at')
    list_filter = ('is_active', 'assigned_at')
    search_fields = ('task__title', 'user__username')
    readonly_fields = ('assign_id', 'assigned_at')
    raw_id_fields = ('task', 'user', 'assigned_by')


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_id', 'list', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('template_id', 'created_at', 'updated_at')
    raw_id_fields = ('list',)


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'field_id', 'field_type', "is_deleted",
                    'template', 'order',
                    'is_required', 'created_by', 'created_at')
    list_filter = ('field_type', 'is_required', 'created_at')
    search_fields = ('field_name', 'description')
    readonly_fields = ('field_id', 'created_at', 'updated_at')
    raw_id_fields = ('template', 'created_by')
    ordering = ('template', 'order')


@admin.register(TaskFieldValue)
class TaskFieldValueAdmin(admin.ModelAdmin):
    list_display = ('field', 'task', 'value', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('field__field_name', 'task__title')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('field', 'task', 'created_by')


@admin.register(ListView)
class ListViewAdmin(admin.ModelAdmin):
    list_display = ('list', 'view_type', 'id', 'is_active', 'created_by',
                    'created_at', 'view_name')
    list_filter = ('view_type', 'is_active', 'created_at')
    search_fields = ('list__name', 'view_type')
    readonly_fields = ('created_at',)
    raw_id_fields = ('list', 'created_by')


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


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "plan_name",
        "billing_period",
        "price",
        "currency",
        "stripe_price_id",
        "is_active",
        "created_at",
    )
    list_filter = ("plan_name", "billing_period", "is_active", "created_at")
    search_fields = ("stripe_price_id", "plan_name")
    readonly_fields = ("plan_id", "created_at", "updated_at")
    ordering = ("plan_name", "billing_period", "price")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "stripe_customer_id",
        "default_payment_method",
        "created_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__username", "user__email", "stripe_customer_id")
    readonly_fields = ("customer_id", "created_at", "updated_at")
    raw_id_fields = ("user",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "subscription_id",
        "user",
        "plan",
        "status",
        "cancel_at_period_end",
        "current_period_end",
        "created_at",
    )
    list_filter = (
        "status",
        "cancel_at_period_end",
        "plan",
        "created_at",
        "current_period_end",
    )
    search_fields = (
        "subscription_id",
        "stripe_subscription_id",
        "user__username",
        "user__email",
    )
    readonly_fields = ("subscription_id", "created_at", "updated_at")
    raw_id_fields = ("user", "plan")
    ordering = ("-created_at",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_id",
        "user",
        "subscription",
        "amount",
        "currency",
        "status",
        "payment_method",
        "created_at",
    )
    list_filter = ("status", "currency", "payment_method", "created_at")
    search_fields = (
        "payment_id",
        "stripe_payment_intent_id",
        "user__username",
        "user__email",
        "subscription__stripe_subscription_id",
    )
    readonly_fields = ("payment_id", "created_at", "updated_at")
    raw_id_fields = ("user", "subscription")
    ordering = ("-created_at",)
