from task_management.interactors.dtos import UserDTO, CreateUserDTO, \
    UpdateUserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import \
    UserStorageInterface
from task_management.models import User


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
        user_obj.image_url = user_data.image_url
        if user_data.gender:
            user_obj.gender = user_data.gender

        if user_data.full_name:
            user_obj.full_name = user_data.full_name


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

    def check_user_username_exists(self, user_id: str, username: str) -> bool:
        return User.objects.filter(username=username).exclude(
            user_id=user_id).exists()

    def check_user_email_exists(self, user_id: str, email: str) -> bool:
        return User.objects.filter(email=email).exclude(
            user_id=user_id).exists()

    def check_phone_number_except_current_user(self, user_id: str,
                                               phone_number: str) -> bool:
        return User.objects.filter(phone_number=phone_number).exclude(
            user_id=user_id).exists()

    def check_user_exists(self, user_id: str)-> bool:
        return User.objects.filter(user_id=user_id).exists()
