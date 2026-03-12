from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import UserDTO
from task_management.tests.api_tests.users import BaseBlockUser


def get_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.get_user"
    )


def block_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.block_user"
    )


def make_user_dto(is_active=True) -> UserDTO:
    return UserDTO(
        user_id="user_1",
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        phone_number="9999999999",
        image_url="https://example.com/image.png",
        is_active=is_active,
        gender=Gender.MALE,
        password="hashed_password",
    )


@pytest.mark.django_db
class TestBlockUserAPI(BaseBlockUser):
    def test_block_user_successfully(self, snapshot, mocker):
        get_user_mock(mocker).return_value = make_user_dto(is_active=True)
        block_user_mock(mocker).return_value = make_user_dto(is_active=False)

        variables = {"params": {"userId": "user_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="admin"),
        )

    def test_block_user_not_found(self, snapshot, mocker):
        get_user_mock(mocker).return_value = None

        variables = {"params": {"userId": "user_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="admin"),
        )

    def test_block_user_inactive(self, snapshot, mocker):
        get_user_mock(mocker).return_value = make_user_dto(is_active=False)

        variables = {"params": {"userId": "user_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="admin"),
        )
