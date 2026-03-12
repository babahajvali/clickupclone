from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import PasswordResetTokenDTO, UserDTO
from task_management.tests.api_tests.users import BaseForgotPassword


def get_user_by_email_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.get_user_by_email"
    )


def create_password_reset_token_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage."
        "create_password_reset_token"
    )


def send_password_reset_email_mock(mocker):
    return mocker.patch(
        "task_management.email_service.email_service.EmailService."
        "send_password_reset_email"
    )


def token_urlsafe_mock(mocker):
    return mocker.patch(
        "task_management.interactors.user.reset_password_interactor.secrets."
        "token_urlsafe",
        return_value="reset_token_123",
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


def make_reset_token_dto() -> PasswordResetTokenDTO:
    return PasswordResetTokenDTO(
        user_id="user_1",
        token="reset_token_123",
        created_at=datetime.now(),
        is_used=False,
        expires_at=datetime.now() + timedelta(hours=1),
    )


@pytest.mark.django_db
class TestForgotPasswordAPI(BaseForgotPassword):
    def test_forgot_password_successfully(self, snapshot, mocker):
        get_user_by_email_mock(mocker).return_value = make_user_dto()
        create_password_reset_token_mock(mocker).return_value = (
            make_reset_token_dto()
        )
        send_password_reset_email_mock(mocker).return_value = True
        token_urlsafe_mock(mocker)

        variables = {"params": {"email": "test@example.com"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_forgot_password_email_not_found(self, snapshot, mocker):
        get_user_by_email_mock(mocker).return_value = None
        token_urlsafe_mock(mocker)

        variables = {"params": {"email": "missing@example.com"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
