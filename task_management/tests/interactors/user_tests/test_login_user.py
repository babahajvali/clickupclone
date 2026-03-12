from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    EmailNotFound,
    InactiveUser,
    IncorrectPassword,
)
from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import UserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface,
)
from task_management.interactors.user.user_login_interactor import (
    UserLoginInteractor,
)


class TestUserLogin:

    @staticmethod
    def _make_user(password: str = "stored_password", is_active: bool = True):
        return UserDTO(
            user_id="user123",
            full_name="Test User",
            username="testuser",
            email="test@email.com",
            phone_number="9999999999",
            password=password,
            gender=Gender.MALE,
            is_active=is_active,
            image_url="https://example.com/image.png",
        )

    def test_user_login_successfully(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        user_storage.get_user_by_email.return_value = self._make_user(
            password="plain_password",
        )

        interactor = UserLoginInteractor(user_storage=user_storage)

        result = interactor.user_login(
            email="test@email.com",
            password="plain_password",
        )

        snapshot.assert_match(
            repr(result.username),
            "test_user_login_successfully.txt",
        )

    def test_user_login_email_not_found(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        user_storage.get_user_by_email.return_value = None

        interactor = UserLoginInteractor(user_storage=user_storage)

        with pytest.raises(EmailNotFound) as exc:
            interactor.user_login(
                email="missing@email.com",
                password="plain_password",
            )

        snapshot.assert_match(
            repr(exc.value),
            "test_user_login_email_not_found.txt",
        )

    def test_user_login_inactive_user(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        user_storage.get_user_by_email.return_value = self._make_user(
            is_active=False,
        )

        interactor = UserLoginInteractor(user_storage=user_storage)

        with pytest.raises(InactiveUser) as exc:
            interactor.user_login(
                email="test@email.com",
                password="plain_password",
            )

        snapshot.assert_match(
            repr(exc.value),
            "test_user_login_inactive_user.txt",
        )

    def test_user_login_incorrect_password(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        user_storage.get_user_by_email.return_value = self._make_user(
            password="different_password",
        )

        interactor = UserLoginInteractor(user_storage=user_storage)

        with pytest.raises(IncorrectPassword) as exc:
            interactor.user_login(
                email="test@email.com",
                password="plain_password",
            )

        snapshot.assert_match(
            repr(exc.value),
            "test_user_login_incorrect_password.txt",
        )
