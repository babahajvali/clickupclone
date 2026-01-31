import uuid
from django.db import models



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