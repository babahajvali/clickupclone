from datetime import datetime

from task_management.interactors.dtos import PasswordResetTokenDTO, UserDTO
from task_management.interactors.storage_interface.password_reset_storage_interface import \
    PasswordResetStorageInterface
from task_management.models.user_models import PasswordResetToken, User


class PasswordResetStorage(PasswordResetStorageInterface):

    def create_password_reset_token(self, user_id: str, token: str,
                                    expires_at: datetime) -> PasswordResetTokenDTO:
        try:
            PasswordResetToken.objects.filter(
                user_id=user_id,
                is_used=False
            ).delete()

            reset_token = PasswordResetToken.objects.create(
                user_id=user_id,
                token=token,
                expires_at=expires_at,
                is_used=False
            )

            return PasswordResetTokenDTO(
                user_id=str(reset_token.user.user_id),
                token=reset_token.token,
                created_at=reset_token.created_at,
                expires_at=reset_token.expires_at
            )

        except Exception as e:
            raise Exception(f"Failed to create password reset token: {str(e)}")

    def get_reset_token(self, token: str) -> PasswordResetTokenDTO | None:
        try:
            reset_token = PasswordResetToken.objects.select_related(
                'user').get(
                token=token,
                is_used=False
            )

            return PasswordResetTokenDTO(
                user_id=str(reset_token.user.user_id),
                token=reset_token.token,
                created_at=reset_token.created_at,
                expires_at=reset_token.expires_at
            )

        except PasswordResetToken.DoesNotExist:
            return None

        except Exception as e:
            raise Exception(f"Failed to get reset token: {str(e)}")

    def used_reset_token(self, token: str) -> bool:

        token_data = PasswordResetToken.objects.get(token=token)
        token_data.is_used = True
        token_data.save()

        return token_data.is_used

    def update_user_password(self, user_id: str, new_password: str) -> UserDTO:
        try:
            user = User.objects.get(user_id=user_id)

            user.password = new_password
            user.save()

            return UserDTO(
                user_id=str(user.user_id),
                full_name=user.full_name,
                gender=user.gender,
                username=user.username,
                email=user.email,
                phone_number=user.phone_number,
                is_active=user.is_active,
                password=None,
                image_url=user.image_url,
            )

        except Exception as e:
            raise Exception(f"Failed to update user password: {str(e)}")
