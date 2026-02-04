from unittest.mock import create_autospec
import pytest

from task_management.exceptions.custom_exceptions import (
    UserNotFoundException,
    InactiveUserException,  # use your actual exception name
)
from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import UserDTO
from task_management.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface,
)
from task_management.interactors.user_interactor.user_interactors import (
    UserInteractor,
)


class TestGetUserProfile:

    def test_get_user_profile_successfully(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)

        user = UserDTO(
            user_id="user123",
            full_name="Test User",
            username="testuser",
            email="test@email.com",
            phone_number="9999999999",
            password="password",
            gender=Gender.MALE.value,
            is_active=True,
            image_url="https://example.com/image.png",
        )

        user_storage.get_user_data.return_value = user

        interactor = UserInteractor(user_storage=user_storage)

        result = interactor.get_user_profile(user_id="user123")

        snapshot.assert_match(
            repr(result.username),
            "test_get_user_profile_successfully.txt",
        )

        user_storage.get_user_data.assert_called_with(user_id="user123")

    def test_get_user_profile_user_not_found(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)

        user_storage.get_user_data.return_value = None

        interactor = UserInteractor(user_storage=user_storage)

        with pytest.raises(UserNotFoundException) as exc:
            interactor.get_user_profile(user_id="user123")

        snapshot.assert_match(
            repr(exc.value),
            "test_get_user_profile_user_not_found.txt",
        )

    def test_get_user_profile_user_inactive(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)

        inactive_user = UserDTO(
            user_id="user123",
            full_name="Inactive User",
            username="inactive",
            email="inactive@email.com",
            phone_number="9999999999",
            password="password",
            gender=Gender.MALE.value,
            is_active=False,
            image_url="url",
        )

        user_storage.get_user_data.return_value = inactive_user

        interactor = UserInteractor(user_storage=user_storage)

        with pytest.raises(InactiveUserException) as exc:
            interactor.get_user_profile(user_id="user123")

        snapshot.assert_match(
            repr(exc.value),
            "test_get_user_profile_user_inactive.txt",
        )
