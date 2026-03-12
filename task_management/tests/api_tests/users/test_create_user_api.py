from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import UserDTO
from task_management.tests.api_tests.users import BaseCreateUser


def check_username_exists_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.check_username_exists"
    )


def check_email_exists_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.check_email_exists"
    )


def check_phone_number_exists_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.check_phone_number_exists"
    )


def create_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.create_user"
    )


def make_user_dto() -> UserDTO:
    return UserDTO(
        user_id="user_1",
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        phone_number="9999999999",
        image_url="https://example.com/image.png",
        is_active=True,
        gender=Gender.MALE,
        password="hashed_password",
    )


@pytest.mark.django_db
class TestCreateUserAPI(BaseCreateUser):
    def _setup_common(self, mocker):
        check_username_exists_mock(mocker).return_value = False
        check_email_exists_mock(mocker).return_value = False
        check_phone_number_exists_mock(mocker).return_value = False

    def test_create_user_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        create_user_mock(mocker).return_value = make_user_dto()

        variables = {
            "params": {
                "username": "testuser",
                "email": "test@example.com",
                "password": "Secret123!",
                "fullName": "Test User",
                "phoneNumber": "9999999999",
                "gender": "MALE",
                "imageUrl": "https://example.com/image.png",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="admin"),
        )

    def test_create_user_username_exists(self, snapshot, mocker):
        self._setup_common(mocker)
        check_username_exists_mock(mocker).return_value = True

        variables = {
            "params": {
                "username": "testuser",
                "email": "test@example.com",
                "password": "Secret123!",
                "fullName": "Test User",
                "phoneNumber": "9999999999",
                "gender": "MALE",
                "imageUrl": "https://example.com/image.png",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="admin"),
        )

    def test_create_user_email_exists(self, snapshot, mocker):
        self._setup_common(mocker)
        check_email_exists_mock(mocker).return_value = True

        variables = {
            "params": {
                "username": "testuser",
                "email": "test@example.com",
                "password": "Secret123!",
                "fullName": "Test User",
                "phoneNumber": "9999999999",
                "gender": "MALE",
                "imageUrl": "https://example.com/image.png",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="admin"),
        )
