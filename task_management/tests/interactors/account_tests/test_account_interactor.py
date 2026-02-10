import pytest
from unittest.mock import create_autospec, Mock

from task_management.interactors.account_interactor.account_interactors import (
    AccountInteractor
)
from task_management.interactors.storage_interface.account_storage_interface import (
    AccountStorageInterface
)
from task_management.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface
)

from task_management.exceptions.custom_exceptions import (
    AccountNameAlreadyExistsException, UserNotAccountOwnerException
)

from task_management.tests.factories.interactor_factory import (
    CreateAccountFactory,
    AccountDTOFactory
)


class TestAccountInteractor:

    def setup_method(self):
        self.account_storage = create_autospec(AccountStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)

        self.interactor = AccountInteractor(
            account_storage=self.account_storage,
            user_storage=self.user_storage,
        )

    def _mock_active_user(self):
        return type("User", (), {"is_active": True})()

    def _mock_account(self, owner_id):
        return type(
            "Account",
            (),
            {"owner_id": owner_id, "is_active": True}
        )()

    # ---------------- CREATE ACCOUNT ---------------- #

    def test_create_account_success(self, snapshot):
        create_data = CreateAccountFactory()
        expected = AccountDTOFactory()

        self.account_storage.validate_account_name_exists.return_value = False
        self.account_storage.create_account.return_value = expected
        self.interactor._create_workspace = Mock()

        result = self.interactor.create_account(create_data)

        snapshot.assert_match(
            repr(result),
            "create_account_success.txt"
        )

    def test_create_account_name_already_exists(self, snapshot):
        create_data = CreateAccountFactory()

        self.account_storage.validate_account_name_exists.return_value = True

        with pytest.raises(AccountNameAlreadyExistsException) as exc:
            self.interactor.create_account(create_data)

        snapshot.assert_match(
            repr(exc.value),
            "create_account_name_already_exists.txt"
        )

    # ---------------- TRANSFER ACCOUNT ---------------- #

    def test_transfer_account_success(self, snapshot):
        account_id = "account-123"
        old_owner_id = "user-123"
        new_owner_id = "user-456"

        existing_account = self._mock_account(old_owner_id)
        expected = AccountDTOFactory(owner_id=new_owner_id)

        self.account_storage.get_account_by_id.return_value = existing_account
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.account_storage.transfer_account.return_value = expected

        result = self.interactor.transfer_account(
            account_id=account_id,
            current_owner_id=old_owner_id,
            new_owner_id=new_owner_id
        )

        snapshot.assert_match(
            repr(result),
            "transfer_account_success.txt"
        )

    def test_transfer_account_non_owner(self, snapshot):
        account_id = "account-123"
        old_owner_id = "owner-123"
        non_owner_id = "user-999"
        new_owner_id = "user-456"

        self.account_storage.get_account_by_id.return_value = \
            self._mock_account(old_owner_id)

        with pytest.raises(UserNotAccountOwnerException) as exc:
            self.interactor.transfer_account(
                account_id=account_id,
                current_owner_id=non_owner_id,
                new_owner_id=new_owner_id
            )

        snapshot.assert_match(
            repr(exc.value),
            "transfer_account_non_owner.txt"
        )

    def test_delete_account_success(self, snapshot):
        account_id = "account-123"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = type(
            "Account",
            (),
            {"is_active": True,
             "owner_id": owner_id}
        )()


        self.account_storage.delete_account.return_value = None

        result = self.interactor.delete_account(
            account_id=account_id,
            deleted_by=owner_id
        )

        snapshot.assert_match(
            repr(result),
            "delete_account_success.txt"
        )

    def test_delete_account_non_owner(self, snapshot):
        account_id = "account-123"
        user_id = "user-999"

        self.account_storage.get_account_by_id.return_value = type(
            "Account",
            (),
            {"is_active": True,
             "owner_id": "some-other-user"}
        )()

        with pytest.raises(UserNotAccountOwnerException) as exc:
            self.interactor.delete_account(
                account_id=account_id,
                deleted_by=user_id
            )

        snapshot.assert_match(
            repr(exc.value),
            "delete_account_non_owner.txt"
        )
