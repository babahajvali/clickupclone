from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import InvalidAccountIds
from task_management.interactors.accounts.get_accounts_interactor import (
    GetAccountsInteractor,
)
from task_management.interactors.storage_interfaces.account_storage_interface import (
    AccountStorageInterface,
)
from task_management.tests.factories.interactor_factory import AccountDTOFactory


class TestGetAccountsInteractor:
    def setup_method(self):
        self.account_storage = create_autospec(AccountStorageInterface)
        self.interactor = GetAccountsInteractor(
            account_storage=self.account_storage,
        )

    def test_get_accounts_success(self, snapshot):
        account_id1 = "12345678-1234-5678-1234-567812345678"
        account_id2 = "12345678-1234-5678-1234-567812345679"

        accounts_data = [
            AccountDTOFactory(
                account_id=account_id1,
                name="Davis Group",
                description="Everyone study professional read.",
                owner_id="e9a90d2d-9d25-473c-9912-be8b01953205",
                is_active=True,
            ),
            AccountDTOFactory(
                account_id=account_id2,
                name="Jensen Inc",
                description="Statement officer down door.",
                owner_id="a85eb996-1280-4afb-9d96-6cc733c6d7c3",
                is_active=True,
            ),
        ]
        self.account_storage.get_existing_account_ids.return_value = [
            account_id1,
            account_id2,
        ]
        self.account_storage.get_accounts.return_value = accounts_data

        result = self.interactor.get_accounts(account_ids=[account_id1, account_id2])

        snapshot.assert_match(repr(result), "get_accounts_success.txt")

    def test_get_accounts_invalid_ids(self, snapshot):
        valid_id = "12345678-1234-5678-1234-567812345678"
        invalid_id = "invalid-id-999"

        mock_account = type("Account", (), {"account_id": valid_id, "is_active": True})()
        self.account_storage.get_accounts.return_value = [mock_account]

        with pytest.raises(InvalidAccountIds) as exc:
            self.interactor.get_accounts(account_ids=[valid_id, invalid_id])

        snapshot.assert_match(repr(exc.value), "get_accounts_invalid_ids.txt")

    def test_get_accounts_empty_list(self, snapshot):
        self.account_storage.get_accounts.return_value = []

        result = self.interactor.get_accounts(account_ids=[])

        snapshot.assert_match(repr(result), "get_accounts_empty_list.txt")
