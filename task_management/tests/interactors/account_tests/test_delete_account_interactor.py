from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import UserNotAccountOwner
from task_management.interactors.accounts.delete_account_interactor import (
    DeleteAccountInteractor,
)
from task_management.interactors.storage_interfaces.account_storage_interface import (
    AccountStorageInterface,
)
from task_management.tests.factories.interactor_factory import AccountDTOFactory


class TestDeleteAccountInteractor:
    def setup_method(self):
        self.account_storage = create_autospec(AccountStorageInterface)
        self.interactor = DeleteAccountInteractor(
            account_storage=self.account_storage,
        )

    @staticmethod
    def _mock_account(owner_id, is_active=True):
        return type("Account", (), {"owner_id": owner_id, "is_active": is_active})()

    def test_delete_account_success(self, snapshot):
        account_id = "accounts-123"
        owner_id = "user-123"
        expected = AccountDTOFactory(
            account_id=account_id,
            owner_id=owner_id,
            is_active=False,
            name="Sample Account",
            description="Sample Account description",
        )

        self.account_storage.get_account.return_value = self._mock_account(owner_id)
        self.account_storage.delete_account.return_value = expected

        result = self.interactor.delete_account(account_id=account_id, deleted_by=owner_id)

        snapshot.assert_match(repr(result), "delete_account_success.txt")

    def test_delete_account_non_owner(self, snapshot):
        account_id = "accounts-123"
        user_id = "user-999"

        self.account_storage.get_account.return_value = self._mock_account("some-other-user")

        with pytest.raises(UserNotAccountOwner) as exc:
            self.interactor.delete_account(account_id=account_id, deleted_by=user_id)

        snapshot.assert_match(repr(exc.value), "delete_account_non_owner.txt")
