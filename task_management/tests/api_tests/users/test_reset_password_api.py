from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import PasswordResetTokenDTO, UserDTO
from task_management.tests.api_tests.users import BaseResetPassword


def get_reset_token_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.get_reset_token"
    )


def update_user_password_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.update_user_password"
    )


def used_reset_token_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.used_reset_token"
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


def make_reset_token_dto(expires_at: datetime) -> PasswordResetTokenDTO:
    return PasswordResetTokenDTO(
        user_id="user_1",
        token="reset_token_123",
        created_at=datetime.now(),
        is_used=False,
        expires_at=expires_at,
    )


@pytest.mark.django_db
class TestResetPasswordAPI(BaseResetPassword):
    def test_reset_password_successfully(self, snapshot, mocker):
        get_reset_token_mock(mocker).return_value = make_reset_token_dto(
            expires_at=datetime.now() + timedelta(hours=1),
        )
        update_user_password_mock(mocker).return_value = make_user_dto()
        used_reset_token_mock(mocker).return_value = True

        variables = {
            "params": {
                "token": "reset_token_123",
                "newPassword": "Secret123!",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reset_password_invalid_token(self, snapshot, mocker):
        get_reset_token_mock(mocker).return_value = None

        variables = {
            "params": {
                "token": "invalid_token",
                "newPassword": "Secret123!",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reset_password_expired_token(self, snapshot, mocker):
        get_reset_token_mock(mocker).return_value = make_reset_token_dto(
            expires_at=datetime.now() - timedelta(hours=1),
        )
        used_reset_token_mock(mocker).return_value = True

        variables = {
            "params": {
                "token": "expired_token",
                "newPassword": "Secret123!",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
