import uuid

from django.db import models



class RoleType(models.TextChoices):
    OWNER = "owner", "Owner"
    ADMIN = "admin", "Admin"
    MEMBER = "member", "Member"
    GUEST = "guest", "Guest"


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