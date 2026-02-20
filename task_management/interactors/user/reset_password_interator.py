import secrets
from datetime import timedelta
from django.utils import timezone

from task_management.interactors.email_service_interface.email_service_interface import \
    EmailServiceInterface
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface

from task_management.mixins import UserValidationMixin


class PasswordResetInteractor(UserValidationMixin):
    def __init__(self, user_storage: UserStorageInterface,
                 email_service: EmailServiceInterface = None,
                 reset_token_expiry_hours: int = 1):
        super().__init__(user_storage=user_storage)
        self.user_storage = user_storage
        self.email_service = email_service
        self.reset_token_expiry_hours = reset_token_expiry_hours

    def request_password_reset(self, email: str, base_url: str) -> bool:

        user_data = self.user_storage.get_user_details(email=email)
        if not user_data:
            from task_management.exceptions.custom_exceptions import \
                EmailNotFound
            raise EmailNotFound(email=email)

        reset_token = secrets.token_urlsafe(32)

        expires_at = timezone.now() + timedelta(
            hours=self.reset_token_expiry_hours)

        self.user_storage.create_password_reset_token(
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

        reset_token_data = self.user_storage.get_reset_token(
            token=token)

        if not reset_token_data:
            from task_management.exceptions.custom_exceptions import \
                InvalidResetToken
            raise InvalidResetToken(token=token)

        if timezone.now() > reset_token_data.expires_at:
            self.user_storage.used_reset_token(token=token)
            from task_management.exceptions.custom_exceptions import \
                ResetTokenExpired
            raise ResetTokenExpired(token=token)

        updated_user = self.user_storage.update_user_password(
            user_id=reset_token_data.user_id,
            new_password=new_password
        )

        self.user_storage.used_reset_token(token=token)

        return updated_user

    def validate_reset_token(self, token: str) -> bool:

        reset_token_data = self.user_storage.get_reset_token(
            token=token)

        if not reset_token_data:
            from task_management.exceptions.custom_exceptions import \
                InvalidResetToken
            raise InvalidResetToken(token=token)

        if reset_token_data.is_used:
            from task_management.exceptions.custom_exceptions import \
                InvalidResetToken
            raise InvalidResetToken(token=token)

        if timezone.now() > reset_token_data.expires_at:
            from task_management.exceptions.custom_exceptions import \
                ResetTokenExpired
            raise ResetTokenExpired(token=token)

        return True
