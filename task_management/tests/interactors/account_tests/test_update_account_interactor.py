from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    AccountNameAlreadyExists,
    AccountNotFound,
    InactiveAccount,
    NothingToUpdateAccount,
    UserNotAccountOwner,
)
from task_management.interactors.accounts.update_account_interactor import (
    UpdateAccountInteractor,
)
from task_management.interactors.storage_interfaces.account_storage_interface import (
    AccountStorageInterface,
)
from task_management.tests.factories.interactor_factory import AccountDTOFactory


class TestUpdateAccountInteractor:
    def setup_method(self):
        self.account_storage = create_autospec(AccountStorageInterface)
        self.interactor = UpdateAccountInteractor(
            account_storage=self.account_storage,
        )

    @staticmethod
    def _mock_account(owner_id, is_active=True):
        return type("Account", (), {"owner_id": owner_id, "is_active": is_active})()

    def test_update_account_name_success(self, snapshot):
        account_id = "accounts-123"
        owner_id = "user-123"

        self.account_storage.get_account.return_value = self._mock_account(owner_id)
        self.account_storage.is_account_name_exists.return_value = False
        expected = AccountDTOFactory(
            account_id="1338682e-aaa6-4bf7-8eb9-f69540d607aa",
            name="Ayala-Reed",
            description="Clearly computer six throw.",
            owner_id="f4e6b609-4092-4639-9925-b5eb8161e704",
            is_active=True,
        )
        self.account_storage.update_account.return_value = expected

        result = self.interactor.update_account(
            account_id=account_id,
            user_id=owner_id,
            name="New Name",
            description=None,
        )

        snapshot.assert_match(repr(result), "update_account_name_success.txt")

    def test_update_account_description_success(self, snapshot):
        account_id = "accounts-123"
        owner_id = "user-123"

        self.account_storage.get_account.return_value = self._mock_account(owner_id)
        expected = AccountDTOFactory(
            account_id="f3d01024-dff6-4e82-913f-90938dd02dd1",
            name="Carroll, Martin and Fitzgerald",
            description="Agree international run process strategy week.",
            owner_id="0d434db0-51ba-4723-bede-d24b660d4351",
            is_active=True,
        )
        self.account_storage.update_account.return_value = expected

        result = self.interactor.update_account(
            account_id=account_id,
            user_id=owner_id,
            name=None,
            description="Updated description",
        )

        snapshot.assert_match(repr(result), "update_account_description_success.txt")

    def test_update_account_both_fields_success(self, snapshot):
        account_id = "accounts-123"
        owner_id = "user-123"

        self.account_storage.get_account.return_value = self._mock_account(owner_id)
        self.account_storage.is_account_name_exists.return_value = False
        expected = AccountDTOFactory(
            account_id="8946ba18-6e40-45e7-83a9-5929fd1701c0",
            name="Serrano-Mcdonald",
            description="Reflect herself operation no game film paper.",
            owner_id="72a7ed06-920d-4fdc-bc76-005d8803299a",
            is_active=True,
        )
        self.account_storage.update_account.return_value = expected

        result = self.interactor.update_account(
            account_id=account_id,
            user_id=owner_id,
            name="New Name",
            description="New Description",
        )

        snapshot.assert_match(repr(result), "update_account_both_fields_success.txt")

    def test_update_account_nothing_to_update(self, snapshot):
        account_id = "accounts-123"
        owner_id = "user-123"

        self.account_storage.get_account.return_value = self._mock_account(owner_id)

        with pytest.raises(NothingToUpdateAccount) as exc:
            self.interactor.update_account(
                account_id=account_id,
                user_id=owner_id,
                name=None,
                description=None,
            )

        snapshot.assert_match(repr(exc.value), "update_account_nothing_to_update.txt")

    def test_update_account_name_already_exists(self, snapshot):
        account_id = "accounts-123"
        owner_id = "user-123"

        self.account_storage.get_account.return_value = self._mock_account(owner_id)
        self.account_storage.is_account_name_exists.return_value = "different-accounts-id"

        with pytest.raises(AccountNameAlreadyExists) as exc:
            self.interactor.update_account(
                account_id=account_id,
                user_id=owner_id,
                name="Taken Name",
                description=None,
            )

        snapshot.assert_match(repr(exc.value), "update_account_name_already_exists.txt")

    def test_update_account_non_owner(self, snapshot):
        account_id = "accounts-123"
        owner_id = "actual-owner"
        other_user = "intruder-user"

        self.account_storage.get_account.return_value = self._mock_account(owner_id)
        self.account_storage.is_account_name_exists.return_value = False

        with pytest.raises(UserNotAccountOwner) as exc:
            self.interactor.update_account(
                account_id=account_id,
                user_id=other_user,
                name="New Name",
                description=None,
            )

        snapshot.assert_match(repr(exc.value), "update_account_non_owner.txt")

    def test_update_account_not_found(self, snapshot):
        account_id = "non-existent-accounts"
        owner_id = "user-123"

        self.account_storage.is_account_name_exists.return_value = False
        self.account_storage.get_account.return_value = None

        with pytest.raises(AccountNotFound) as exc:
            self.interactor.update_account(
                account_id=account_id,
                user_id=owner_id,
                name="Name",
                description=None,
            )

        snapshot.assert_match(repr(exc.value), "update_account_not_found.txt")

    def test_update_account_inactive(self, snapshot):
        account_id = "accounts-123"
        owner_id = "user-123"

        self.account_storage.is_account_name_exists.return_value = False
        self.account_storage.get_account.return_value = self._mock_account(
            owner_id, is_active=False
        )

        with pytest.raises(InactiveAccount) as exc:
            self.interactor.update_account(
                account_id=account_id,
                user_id=owner_id,
                name="New Name",
                description=None,
            )

        snapshot.assert_match(repr(exc.value), "update_account_inactive.txt")
