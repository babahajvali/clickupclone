from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import UserDTO
from task_management.tests.api_tests.users import BaseUserLogin


def get_user_by_email_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.get_user_by_email"
    )


def generate_access_token_mock(mocker):
    return mocker.patch(
        "task_management.graphql.mutations.user.user_login_mutation."
        "UserLoginMutation._generate_access_token",
        return_value="token_123",
    )


def make_user_dto(password="plain_password", is_active=True) -> UserDTO:
    return UserDTO(
        user_id="user_1",
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        phone_number="9999999999",
        image_url="https://example.com/image.png",
        is_active=is_active,
        gender=Gender.MALE,
        password=password,
    )


@pytest.mark.django_db
class TestUserLoginAPI(BaseUserLogin):
    def test_user_login_successfully(self, snapshot, mocker):
        get_user_by_email_mock(mocker).return_value = make_user_dto()
        generate_access_token_mock(mocker)

        variables = {
            "params": {
                "email": "test@example.com",
                "password": "plain_password",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_user_login_email_not_found(self, snapshot, mocker):
        get_user_by_email_mock(mocker).return_value = None

        variables = {
            "params": {
                "email": "missing@example.com",
                "password": "plain_password",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_user_login_incorrect_password(self, snapshot, mocker):
        get_user_by_email_mock(mocker).return_value = make_user_dto(
            password="different_password",
        )

        variables = {
            "params": {
                "email": "test@example.com",
                "password": "plain_password",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
