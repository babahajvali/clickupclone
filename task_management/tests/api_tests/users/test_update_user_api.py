from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import UserDTO
from task_management.tests.api_tests.users import BaseUpdateUser


def get_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.get_user"
    )


def check_username_except_current_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage."
        "check_username_except_current_user"
    )


def check_email_exists_except_current_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage."
        "check_email_exists_except_current_user"
    )


def check_phone_number_except_current_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage."
        "check_phone_number_except_current_user"
    )


def update_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.update_user"
    )


def make_user_dto(is_active=True) -> UserDTO:
    return UserDTO(
        user_id="user_1",
        username="updateduser",
        email="updated@example.com",
        full_name="Updated User",
        phone_number="9999999999",
        image_url="https://example.com/image.png",
        is_active=is_active,
        gender=Gender.MALE,
        password="hashed_password",
    )


@pytest.mark.django_db
class TestUpdateUserAPI(BaseUpdateUser):
    def _setup_common(self, mocker, is_active=True):
        get_user_mock(mocker).return_value = make_user_dto(is_active=is_active)
        check_username_except_current_user_mock(mocker).return_value = False
        check_email_exists_except_current_user_mock(mocker).return_value = False
        check_phone_number_except_current_user_mock(mocker).return_value = False

    def test_update_user_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        update_user_mock(mocker).return_value = make_user_dto()

        variables = {
            "params": {
                "username": "updateduser",
                "email": "updated@example.com",
                "fullName": "Updated User",
                "phoneNumber": "9999999999",
                "gender": "MALE",
                "imageUrl": "https://example.com/image.png",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_user_not_found(self, snapshot, mocker):
        get_user_mock(mocker).return_value = None

        variables = {"params": {"username": "updateduser"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_404"),
        )

    def test_update_user_username_exists(self, snapshot, mocker):
        self._setup_common(mocker)
        check_username_except_current_user_mock(mocker).return_value = True

        variables = {"params": {"username": "updateduser"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
