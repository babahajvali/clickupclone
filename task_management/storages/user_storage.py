from datetime import datetime

from django.contrib.auth.hashers import make_password

from task_management.interactors.dtos import UserDTO, CreateUserDTO, \
    UpdateUserDTO, PasswordResetTokenDTO
from task_management.interactors.storage_interfaces import UserStorageInterface
from task_management.models import User, PasswordResetToken


class UserStorage(UserStorageInterface):

    @staticmethod
    def _convert_user_to_dto(user_obj: User) -> UserDTO:
        return UserDTO(
            user_id=user_obj.user_id,
            username=user_obj.username,
            email=user_obj.email,
            password=user_obj.password,
            full_name=user_obj.full_name,
            phone_number=user_obj.phone_number,
            image_url=user_obj.image_url,
            is_active=user_obj.is_active,
            gender=user_obj.gender,
        )

    def get_user(self, user_id: str) -> UserDTO | None:

        user_obj = User.objects.filter(user_id=user_id).first()
        if user_obj is None:
            return None

        return self._convert_user_to_dto(user_obj=user_obj)

    def get_user_by_email(self, email: str) -> UserDTO | None:

        user_obj = User.objects.filter(email=email).first()

        if user_obj is None:
            return None

        return self._convert_user_to_dto(user_obj=user_obj)

    def create_user(self, create_user_dto: CreateUserDTO) -> UserDTO:
        user_obj = User.objects.create(
            username=create_user_dto.username,
            full_name=create_user_dto.full_name,
            email=create_user_dto.email,
            phone_number=create_user_dto.phone_number,
            image_url=create_user_dto.image_url,
            password=make_password(create_user_dto.password),
            gender=create_user_dto.gender.value,
        )

        return self._convert_user_to_dto(user_obj=user_obj)

    def update_user(self, update_user_dto: UpdateUserDTO) -> UserDTO:

        user_properties = {}
        if update_user_dto.username is not None:
            user_properties['username'] = update_user_dto.username
        if update_user_dto.email is not None:
            user_properties['email'] = update_user_dto.email
        if update_user_dto.phone_number is not None:
            user_properties['phone_number'] = update_user_dto.phone_number
        if update_user_dto.gender is not None:
            user_properties['gender'] = update_user_dto.gender.value
        if update_user_dto.full_name is not None:
            user_properties['full_name'] = update_user_dto.full_name
        if update_user_dto.image_url is not None:
            user_properties['image_url'] = update_user_dto.image_url

        User.objects.filter(user_id=update_user_dto.user_id).update(
            **user_properties)

        return self.get_user(user_id=update_user_dto.user_id)

    def block_user(self, user_id: str) -> UserDTO:
        User.objects.filter(user_id=user_id).update(is_active=False)

        return self.get_user(user_id=user_id)

    def check_username_exists(self, username: str) -> bool:
        return User.objects.filter(username=username).exists()

    def check_email_exists(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

    def check_phone_number_exists(self, phone_number: str) -> bool:
        return User.objects.filter(phone_number=phone_number).exists()

    def check_username_except_current_user(
            self, user_id: str, username: str) -> bool:
        return User.objects.filter(username=username).exclude(
            user_id=user_id).exists()

    def check_email_exists_except_current_user(
            self, user_id: str, email: str) -> bool:
        return User.objects.filter(email=email).exclude(
            user_id=user_id).exists()

    def check_phone_number_except_current_user(
            self, user_id: str, phone_number: str) -> bool:
        return User.objects.filter(phone_number=phone_number).exclude(
            user_id=user_id).exists()

    def check_user_exists(self, user_id: str) -> bool:
        return User.objects.filter(user_id=user_id).exists()

    def create_password_reset_token(
            self, user_id: str, token: str, expires_at: datetime) \
            -> PasswordResetTokenDTO:
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
                is_used=reset_token.is_used,
                expires_at=reset_token.expires_at
            )

        except Exception as e:
            raise Exception(
                f"Failed to create password reset token: {str(e)}") from e

    def get_reset_token(self, token: str) -> PasswordResetTokenDTO | None:
        try:
            reset_token = PasswordResetToken.objects.select_related(
                'user').get(token=token, is_used=False)

            return PasswordResetTokenDTO(
                user_id=str(reset_token.user.user_id),
                token=reset_token.token,
                is_used=reset_token.is_used,
                created_at=reset_token.created_at,
                expires_at=reset_token.expires_at
            )

        except PasswordResetToken.DoesNotExist:
            return None

        except Exception as e:
            raise Exception(f"Failed to get reset token: {str(e)}") from e

    def used_reset_token(self, token: str) -> bool:

        updated = PasswordResetToken.objects.filter(token=token).update(
            is_used=True)

        return updated > 0

    def update_user_password(self, user_id: str, new_password: str) -> UserDTO:
        try:
            user_data = User.objects.get(user_id=user_id)

            user_data.password = make_password(new_password)
            user_data.save()

            return UserDTO(
                user_id=str(user_data.user_id),
                full_name=user_data.full_name,
                gender=user_data.gender,
                username=user_data.username,
                email=user_data.email,
                phone_number=user_data.phone_number,
                is_active=user_data.is_active,
                image_url=user_data.image_url,
                password=user_data.password,
            )

        except Exception as e:
            raise Exception(f"Failed to update user password: {str(e)}") from e
