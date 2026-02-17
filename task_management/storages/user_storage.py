from datetime import datetime

from task_management.interactors.dtos import UserDTO, CreateUserDTO, \
    UpdateUserDTO, PasswordResetTokenDTO
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from task_management.models import User, PasswordResetToken


class UserStorage(UserStorageInterface):

    @staticmethod
    def _user_dto(data: User) -> UserDTO:
        return UserDTO(
            user_id=data.user_id,
            username=data.username,
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            phone_number=data.phone_number,
            image_url=data.image_url,
            is_active=data.is_active,
            gender=data.gender,
        )

    def get_user_data(self, user_id: str) -> UserDTO | None:
        try:
            user_data = User.objects.get(user_id=user_id)
            return self._user_dto(data=user_data)
        except User.DoesNotExist:
            return None

    def get_user_details(self, email: str) -> UserDTO | None:
        try:
            user_data = User.objects.get(email=email)
            return self._user_dto(data=user_data)
        except User.DoesNotExist:
            return None

    def create_user(self, user_data: CreateUserDTO) -> UserDTO:
        user_obj = User.objects.create(
            username=user_data.username, full_name=user_data.full_name,
            email=user_data.email, phone_number=user_data.phone_number,
            image_url=user_data.image_url, password=user_data.password,
            gender=user_data.gender.value,
        )

        return self._user_dto(data=user_obj)

    def update_user(self, user_data: UpdateUserDTO) -> UserDTO:
        user_obj = User.objects.get(user_id=user_data.user_id)
        if user_data.username:
            user_obj.username = user_data.username
        if user_data.email:
            user_obj.email = user_data.email
        if user_data.phone_number:
            user_obj.phone_number = user_data.phone_number
        if user_data.gender:
            user_obj.gender = user_data.gender
        if user_data.full_name:
            user_obj.full_name = user_data.full_name
        user_obj.image_url = user_data.image_url

        user_obj.save()

        return self._user_dto(data=user_obj)

    def block_user(self, user_id: str) -> UserDTO:
        user_obj = User.objects.get(user_id=user_id)
        user_obj.is_active = False
        user_obj.save()

        return self._user_dto(data=user_obj)

    def check_username_exists(self, username: str) -> bool:
        return User.objects.filter(username=username).exists()

    def check_email_exists(self, email: str) -> bool:
        return User.objects.filter(email=email).exists()

    def check_phone_number_exists(self, phone_number: str) -> bool:
        return User.objects.filter(phone_number=phone_number).exists()

    def check_username_except_current_user(self, user_id: str, username: str) -> bool:
        return User.objects.filter(username=username).exclude(
            user_id=user_id).exists()

    def check_email_exists_except_current_user(self, user_id: str, email: str) -> bool:
        return User.objects.filter(email=email).exclude(
            user_id=user_id).exists()

    def check_phone_number_except_current_user(self, user_id: str,
                                               phone_number: str) -> bool:
        return User.objects.filter(phone_number=phone_number).exclude(
            user_id=user_id).exists()

    def check_user_exists(self, user_id: str)-> bool:
        return User.objects.filter(user_id=user_id).exists()

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
                is_used=reset_token.is_used,
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
                is_used=reset_token.is_used,
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
