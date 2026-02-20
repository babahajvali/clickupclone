from unittest.mock import create_autospec
import pytest

from task_management.exceptions.custom_exceptions import (
    UsernameAlreadyExists,
    EmailAlreadyExists,
    PhoneNumberAlreadyExists,
)
from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import UserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface,
)
from task_management.interactors.user.user_interactor import (
    UserInteractor,
)


class TestUpdateUser:

    def _mock_storage_defaults(self, user_storage):
        user_storage.get_user_data.return_value = type(
            "User", (), {"is_active": True}
        )()

        user_storage.check_username_except_current_user.return_value = False
        user_storage.check_username_exists.return_value = False

        user_storage.check_email_exists_except_current_user.return_value = False
        user_storage.check_email_exists.return_value = False

        user_storage.check_phone_number_except_current_user.return_value = False
        user_storage.check_phone_number_exists.return_value = False

    def test_update_user_successfully(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        self._mock_storage_defaults(user_storage)

        updated_user = UserDTO(
            user_id="user123",
            full_name="Updated Name",
            username="updated_username",
            email="updated@email.com",
            phone_number="9999999999",
            password="password",
            gender=Gender.MALE.value,
            is_active=True,
            image_url="https://example.com/image.png",
        )

        user_storage.update_user.return_value = updated_user

        interactor = UserInteractor(user_storage=user_storage)

        result = interactor.update_user(updated_user)

        snapshot.assert_match(
            repr(result.username),
            "test_update_user_successfully.txt",
        )

        user_storage.update_user.assert_called_once_with(
            user_data=updated_user
        )

    def test_update_user_raises_username_exception(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        self._mock_storage_defaults(user_storage)

        user_storage.check_username_except_current_user.return_value = True

        interactor = UserInteractor(user_storage=user_storage)

        user_data = UserDTO(
            user_id="user123",
            full_name="Name",
            username="taken_username",
            email="email@test.com",
            phone_number="9999999999",
            password="password",
            gender=Gender.MALE.value,
            is_active=True,
            image_url="url",
        )

        with pytest.raises(UsernameAlreadyExists) as exc:
            interactor.update_user(user_data)

        snapshot.assert_match(
            repr(exc.value.username),
            "test_update_user_raises_username_exception.txt",
        )

    def test_update_user_raises_email_exception(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        self._mock_storage_defaults(user_storage)

        user_storage.check_email_exists_except_current_user.return_value = True

        interactor = UserInteractor(user_storage=user_storage)

        user_data = UserDTO(
            user_id="user123",
            full_name="Name",
            username="username",
            email="existing@email.com",
            phone_number="9999999999",
            password="password",
            gender=Gender.MALE.value,
            is_active=True,
            image_url="url",
        )

        with pytest.raises(EmailAlreadyExists) as exc:
            interactor.update_user(user_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_update_user_raises_email_exception.txt",
        )

    def test_update_user_raises_phone_exception(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        self._mock_storage_defaults(user_storage)

        user_storage.check_phone_number_except_current_user.return_value = True

        interactor = UserInteractor(user_storage=user_storage)

        user_data = UserDTO(
            user_id="user123",
            full_name="Name",
            username="username",
            email="email@test.com",
            phone_number="existing_phone",
            password="password",
            gender=Gender.MALE.value,
            is_active=True,
            image_url="url",
        )

        with pytest.raises(PhoneNumberAlreadyExists) as exc:
            interactor.update_user(user_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_update_user_raises_phone_exception.txt",
        )
