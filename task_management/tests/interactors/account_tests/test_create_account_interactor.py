from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    AccountNameAlreadyExists,
    EmptyAccountName,
    InactiveUser,
    UserNotFound,
)
from task_management.interactors.accounts.create_account_interactor import (
    CreateAccountInteractor,
)
from task_management.interactors.storage_interfaces.account_storage_interface import (
    AccountStorageInterface,
)
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface,
)
from task_management.tests.factories.interactor_factory import \
    AccountDTOFactory


class TestCreateAccountInteractor:
    def setup_method(self):
        self.account_storage = create_autospec(AccountStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.interactor = CreateAccountInteractor(
            account_storage=self.account_storage,
            user_storage=self.user_storage,
        )

    @staticmethod
    def _mock_active_user():
        return type("User", (), {"is_active": True})()

    def test_create_account_success(self, snapshot):
        expected = AccountDTOFactory(
            account_id="f47d2b4c-1759-4e56-904c-563496a0798a",
            name="Smith PLC",
            description="Reflect hand away.",
            owner_id="3f62e243-07a2-4971-a935-cdd957aa85e3",
            is_active=True,
        )
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.user_storage.get_user.return_value = self._mock_active_user()
        self.account_storage.is_account_name_exists.return_value = False
        self.account_storage.create_account.return_value = expected

        result = self.interactor.create_account(
            name="Sample Account",
            description="Sample Account description",
            created_by=owner_id,
        )

        snapshot.assert_match(repr(result), "create_account_success.txt")

    def test_create_account_name_already_exists(self, snapshot):
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.user_storage.get_user.return_value = self._mock_active_user()
        self.account_storage.is_account_name_exists.return_value = type(
            "Account", (), {"is_active": True, "owner_id": owner_id}
        )

        with pytest.raises(AccountNameAlreadyExists) as exc:
            self.interactor.create_account(
                name="Sample Account",
                description="Sample Account description",
                created_by=owner_id,
            )

        snapshot.assert_match(repr(exc.value),
                              "create_account_name_already_exists.txt")

    def test_empty_account_name_exists(self, snapshot):
        owner_id = "12345678-1234-5678-1234-567812345678"
        self.user_storage.get_user.return_value = self._mock_active_user()
        self.account_storage.is_account_name_exists.return_value = None

        with pytest.raises(EmptyAccountName) as exc:
            self.interactor.create_account(
                name="",
                description="Sample Account description",
                created_by=owner_id,
            )

        snapshot.assert_match(repr(exc.value),
                              "create_empty_account_name_exists.txt")

    def test_create_account_whitespace_name(self, snapshot):
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.user_storage.get_user.return_value = self._mock_active_user()

        with pytest.raises(EmptyAccountName) as exc:
            self.interactor.create_account(
                name="   ",
                description="desc",
                created_by=owner_id,
            )

        snapshot.assert_match(repr(exc.value),
                              "create_account_whitespace_name.txt")

    def test_create_account_non_owner(self, snapshot):
        owner_id = "some-other-user"

        self.user_storage.get_user.return_value = None

        with pytest.raises(UserNotFound) as exc:
            self.interactor.create_account(
                name="Sample Account",
                description="Sample Account description",
                created_by=owner_id,
            )

        snapshot.assert_match(repr(exc.value), "create_account_non_owner.txt")

    def test_create_account_inactive_user(self, snapshot):
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.user_storage.get_user.return_value = type(
            "User", (), {"is_active": False}
        )()

        with pytest.raises(InactiveUser) as exc:
            self.interactor.create_account(
                name="Sample Account",
                description="Sample Account description",
                created_by=owner_id,
            )

        snapshot.assert_match(repr(exc.value),
                              "create_account_inactive_user.txt")

    def test_create_account_with_no_description(self, snapshot):
        expected = AccountDTOFactory(
            account_id="41991bf7-b7ba-43f1-a28a-b9cd4e37af45",
            name="Brooks-Sanchez",
            description="Modern eye institution sort anything face could.",
            owner_id="abc46003-71f8-4851-86f7-f18e117e5314",
            is_active=True,
        )
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.user_storage.get_user.return_value = self._mock_active_user()
        self.account_storage.is_account_name_exists.return_value = False
        self.account_storage.create_account.return_value = expected

        result = self.interactor.create_account(
            name="No Desc Account",
            description=None,
            created_by=owner_id,
        )

        snapshot.assert_match(repr(result),
                              "create_account_no_description.txt")
