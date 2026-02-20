from unittest.mock import create_autospec
import pytest

from task_management.exceptions.custom_exceptions import (
    UserNotFound,
    InactiveUser,  # use your real exception name
)
from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import UserDTO
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface,
)
from task_management.interactors.user.user_interactor import (
    UserInteractor,
)


class TestBlockUser:

    def test_block_user_successfully(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)

        active_user = UserDTO(
            user_id="user123",
            full_name="User",
            username="user",
            email="user@email.com",
            phone_number="9999999999",
            password="password",
            gender=Gender.MALE.value,
            is_active=True,
            image_url="url",
        )

        blocked_user = UserDTO(
            **{**active_user.__dict__, "is_active": False}
        )

        user_storage.get_user_data.return_value = active_user
        user_storage.block_user.return_value = blocked_user

        interactor = UserInteractor(user_storage=user_storage)

        result = interactor.block_user(user_id="user123")

        snapshot.assert_match(
            repr(result.is_active),
            "test_block_user_successfully.txt",
        )

        user_storage.block_user.assert_called_once_with(user_id="user123")

    def test_block_user_user_not_found(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)
        user_storage.get_user_data.return_value = None

        interactor = UserInteractor(user_storage=user_storage)

        with pytest.raises(UserNotFound) as exc:
            interactor.block_user(user_id="user123")

        snapshot.assert_match(
            repr(exc.value),
            "test_block_user_user_not_found.txt",
        )

    def test_block_user_user_inactive(self, snapshot):
        user_storage = create_autospec(UserStorageInterface)

        inactive_user = UserDTO(
            user_id="user123",
            full_name="Inactive",
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

        with pytest.raises(InactiveUser) as exc:
            interactor.block_user(user_id="user123")

        snapshot.assert_match(
            repr(exc.value),
            "test_block_user_user_inactive.txt",
        )
