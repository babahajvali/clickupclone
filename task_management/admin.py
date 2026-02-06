from django.contrib import admin
from task_management.models import (
    User, Account, Workspace, WorkspaceMember,
    Space, SpacePermission, Folder, FolderPermission,
    List, ListPermission, Task, TaskAssignee,
    Template, Field, FieldValue, View, ListView
)
from task_management.models.user_models import PasswordResetToken


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
                    'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
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
    list_display = ('name', 'space_id', 'workspace', 'order', 'is_active',
                    'is_private',
                    'created_by', 'created_at')
    list_filter = ('is_active', 'is_private', 'created_at')
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
    list_display = ('name', 'folder_id', 'space', 'order', 'is_active',
                    'is_private',
                    'created_by', 'created_at')
    list_filter = ('is_active', 'is_private', 'created_at')
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
    list_display = ('name', 'list_id', 'space', 'folder', 'order', 'is_active',
                    'is_private', 'created_by', 'created_at')
    list_filter = ('is_active', 'is_private', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('list_id', 'created_at', 'updated_at')
    raw_id_fields = ('space', 'folder', 'created_by')
    ordering = ('space', 'order')


@admin.register(ListPermission)
class ListPermissionAdmin(admin.ModelAdmin):
    list_display = ('list', 'user', 'permission_type', 'is_active', 'added_by',
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
    list_display = ('field_name', 'field_id', 'field_type', "is_active",
                    'template', 'order',
                    'is_required', 'created_by', 'created_at')
    list_filter = ('field_type', 'is_required', 'created_at')
    search_fields = ('field_name', 'description')
    readonly_fields = ('field_id', 'created_at', 'updated_at')
    raw_id_fields = ('template', 'created_by')
    ordering = ('template', 'order')


@admin.register(FieldValue)
class FieldValueAdmin(admin.ModelAdmin):
    list_display = ('field', 'task', 'value', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('field__field_name', 'task__title')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('field', 'task', 'created_by')


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('name', 'view_id', 'view_type', 'created_by', 'created_at')
    list_filter = ('view_type', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('view_id', 'created_at', 'updated_at')
    raw_id_fields = ('created_by',)


@admin.register(ListView)
class ListViewAdmin(admin.ModelAdmin):
    list_display = ('list', 'view', 'is_active', 'applied_by', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('list__name', 'view__name')
    readonly_fields = ('created_at',)
    raw_id_fields = ('list', 'view', 'applied_by')


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


# task_management/admin.py (or task_management/admin/subscription_admin.py)

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from task_management.models.payment_models import Plan, Customer, Subscription, \
    Payment


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'plan_name',
        'billing_period',
        'price_display',
        'stripe_price_id',
        'is_active',
        'subscription_count',
        'created_at',
    )
    list_filter = ('plan_name', 'billing_period', 'is_active', 'created_at')
    search_fields = ('plan_name', 'stripe_price_id')
    readonly_fields = ('plan_id', 'created_at', 'updated_at')
    ordering = ('plan_name', 'billing_period')

    fieldsets = (
        ('Basic Information', {
            'fields': ('plan_id', 'plan_name', 'billing_period', 'is_active')
        }),
        ('Pricing', {
            'fields': ('price', 'currency', 'stripe_price_id')
        }),
        ('Features', {
            'fields': ('features',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def price_display(self, obj):
        return f"{obj.currency} {obj.price}"

    price_display.short_description = 'Price'

    def subscription_count(self, obj):
        count = obj.subscriptions.count()
        url = reverse(
            'admin:task_management_subscription_changelist') + f'?plan__plan_id__exact={obj.plan_id}'
        return format_html('<a href="{}">{} subscriptions</a>', url, count)

    subscription_count.short_description = 'Active Subscriptions'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('subscriptions')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'customer_id',
        'user_link',
        'stripe_customer_id',
        'has_payment_method',
        'subscription_count',
        'created_at',
    )
    list_filter = ('created_at',)
    search_fields = (
        'user__username',
        'user__email',
        'stripe_customer_id',
        'customer_id',
    )
    readonly_fields = ('customer_id', 'created_at', 'updated_at')
    raw_id_fields = ('user',)

    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_id', 'user', 'stripe_customer_id')
        }),
        ('Payment Details', {
            'fields': ('default_payment_method',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = 'User'

    def has_payment_method(self, obj):
        if obj.default_payment_method:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')

    has_payment_method.short_description = 'Payment Method'

    def subscription_count(self, obj):
        count = obj.user.subscriptions.count()
        url = reverse(
            'admin:task_management_subscription_changelist') + f'?user__id__exact={obj.user.id}'
        return format_html('<a href="{}">{}</a>', url, count)

    subscription_count.short_description = 'Subscriptions'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'subscription_id_short',
        'user_link',
        'plan_link',
        'status_display',
        'current_period_start',
        'current_period_end',
        'cancel_at_period_end',
        'payment_count',
    )
    list_filter = (
        'status',
        'cancel_at_period_end',
        'plan__plan_name',
        'plan__billing_period',
        'created_at',
    )
    search_fields = (
        'user__username',
        'user__email',
        'stripe_subscription_id',
        'subscription_id',
    )
    readonly_fields = (
        'subscription_id',
        'created_at',
        'updated_at',
        'stripe_subscription_id',
    )
    raw_id_fields = ('user', 'plan')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Subscription Information', {
            'fields': (
                'subscription_id',
                'user',
                'plan',
                'stripe_subscription_id',
                'status',
            )
        }),
        ('Billing Period', {
            'fields': (
                'current_period_start',
                'current_period_end',
            )
        }),
        ('Cancellation', {
            'fields': (
                'cancel_at_period_end',
                'canceled_at',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def subscription_id_short(self, obj):
        return str(obj.subscription_id)[:8] + '...'

    subscription_id_short.short_description = 'ID'

    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = 'User'

    def plan_link(self, obj):
        if obj.plan:
            url = reverse('admin:task_management_plan_change',
                          args=[obj.plan.plan_id])
            return format_html('<a href="{}">{}</a>', url, obj.plan.plan_name)
        return '-'

    plan_link.short_description = 'Plan'

    def status_display(self, obj):
        colors = {
            'active': 'green',
            'trialing': 'blue',
            'canceled': 'gray',
            'past_due': 'orange',
            'unpaid': 'red',
            'incomplete': 'orange',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )

    status_display.short_description = 'Status'

    def payment_count(self, obj):
        count = obj.payments.count()
        url = reverse(
            'admin:task_management_payment_changelist') + f'?subscription__subscription_id__exact={obj.subscription_id}'
        return format_html('<a href="{}">{} payments</a>', url, count)

    payment_count.short_description = 'Payments'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'plan').prefetch_related('payments')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payment_id_short',
        'user_link',
        'subscription_link',
        'amount_display',
        'status_display',
        'payment_method',
        'created_at',
    )
    list_filter = (
        'status',
        'currency',
        'created_at',
    )
    search_fields = (
        'user__username',
        'user__email',
        'stripe_payment_intent_id',
        'payment_id',
    )
    readonly_fields = (
        'payment_id',
        'stripe_payment_intent_id',
        'created_at',
        'updated_at',
    )
    raw_id_fields = ('user', 'subscription')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Payment Information', {
            'fields': (
                'payment_id',
                'user',
                'subscription',
                'stripe_payment_intent_id',
                'status',
            )
        }),
        ('Amount', {
            'fields': (
                'amount',
                'currency',
            )
        }),
        ('Payment Method', {
            'fields': ('payment_method',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def payment_id_short(self, obj):
        return str(obj.payment_id)[:8] + '...'

    payment_id_short.short_description = 'ID'

    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    user_link.short_description = 'User'

    def subscription_link(self, obj):
        if obj.subscription:
            url = reverse('admin:task_management_subscription_change',
                          args=[obj.subscription.subscription_id])
            return format_html('<a href="{}">View Subscription</a>', url)
        return '-'

    subscription_link.short_description = 'Subscription'

    def amount_display(self, obj):
        return f"{obj.currency} {obj.amount}"

    amount_display.short_description = 'Amount'

    def status_display(self, obj):
        colors = {
            'succeeded': 'green',
            'pending': 'orange',
            'failed': 'red',
            'canceled': 'gray',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )

    status_display.short_description = 'Status'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'subscription')