from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest

from task_management.interactors.dtos import PasswordResetTokenDTO
from task_management.tests.api_tests.users import BaseValidateResetToken


def get_reset_token_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.get_reset_token"
    )


def make_reset_token_dto(
        *,
        is_used: bool = False,
        expires_at: datetime) -> PasswordResetTokenDTO:
    return PasswordResetTokenDTO(
        user_id="user_1",
        token="reset_token_123",
        created_at=datetime.now(),
        is_used=is_used,
        expires_at=expires_at,
    )


@pytest.mark.django_db
class TestValidateResetTokenAPI(BaseValidateResetToken):
    def test_validate_reset_token_successfully(self, snapshot, mocker):
        get_reset_token_mock(mocker).return_value = make_reset_token_dto(
            expires_at=datetime.now() + timedelta(hours=1),
        )

        variables = {"token": "reset_token_123"}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_validate_reset_token_invalid_token(self, snapshot, mocker):
        get_reset_token_mock(mocker).return_value = None

        variables = {"token": "invalid_token"}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_validate_reset_token_expired(self, snapshot, mocker):
        get_reset_token_mock(mocker).return_value = make_reset_token_dto(
            expires_at=datetime.now() - timedelta(hours=1),
        )

        variables = {"token": "expired_token"}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
