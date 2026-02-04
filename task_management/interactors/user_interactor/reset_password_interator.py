import secrets
from datetime import timedelta
from django.utils import timezone

from task_management.interactors.email_service_interface.email_service_interface import \
    EmailServiceInterface
from task_management.interactors.storage_interface.password_reset_storage_interface import \
    PasswordResetStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface

from task_management.interactors.validation_mixin import ValidationMixin


class PasswordResetInteractor(ValidationMixin):
    def __init__(self, password_reset_storage: PasswordResetStorageInterface,
                 user_storage: UserStorageInterface,
                 email_service: EmailServiceInterface = None,
                 reset_token_expiry_hours: int = 1):
        self.password_reset_storage = password_reset_storage
        self.user_storage = user_storage
        self.email_service = email_service
        self.reset_token_expiry_hours = reset_token_expiry_hours

    def request_password_reset(self, email: str, base_url: str) -> bool:
        """Request password reset for a user"""

        # Check if user exists
        user_data = self.user_storage.get_user_details(email=email)
        if not user_data:
            from task_management.exceptions.custom_exceptions import \
                EmailNotFoundException
            raise EmailNotFoundException(email=email)

        reset_token = secrets.token_urlsafe(32)

        expires_at = timezone.now() + timedelta(
            hours=self.reset_token_expiry_hours)

        self.password_reset_storage.create_password_reset_token(
            user_id=user_data.user_id,
            token=reset_token,
            expires_at=expires_at
        )

        reset_link = f"{base_url}/reset-password?token={reset_token}"

        if self.email_service:
            return self.email_service.send_password_reset_email(
                email=email,
                reset_link=reset_link
            )

        return False

    def reset_password(self, token: str, new_password: str):
        """Reset user password using token"""

        reset_token_data = self.password_reset_storage.get_reset_token(
            token=token)

        if not reset_token_data:
            from task_management.exceptions.custom_exceptions import \
                InvalidResetTokenException
            raise InvalidResetTokenException(token=token)

        if timezone.now() > reset_token_data.expires_at:
            self.password_reset_storage.used_reset_token(token=token)
            from task_management.exceptions.custom_exceptions import \
                ResetTokenExpiredException
            raise ResetTokenExpiredException(token=token)

        updated_user = self.password_reset_storage.update_user_password(
            user_id=reset_token_data.user_id,
            new_password=new_password
        )

        self.password_reset_storage.used_reset_token(token=token)

        return updated_user
