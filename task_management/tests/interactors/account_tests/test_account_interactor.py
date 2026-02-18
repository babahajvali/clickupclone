import pytest
from unittest.mock import create_autospec, Mock

from task_management.interactors.account.account_interactor import \
    AccountInteractor
from task_management.interactors.storage_interfaces.account_storage_interface import (
    AccountStorageInterface
)
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    AccountNameAlreadyExistsException, UserNotAccountOwnerException
)
from task_management.tests.factories.interactor_factory import \
    AccountDTOFactory


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

    def test_create_account_success(self, snapshot):
        expected = AccountDTOFactory()
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.account_storage.validate_account_name_exists.return_value = False
        self.account_storage.create_account.return_value = expected
        self.interactor._create_workspace = Mock()

        result = self.interactor.create_account(
            name="Sample Account", description="Sample Account description",
            created_by=owner_id)

        snapshot.assert_match(
            repr(result),
            "create_account_success.txt"
        )

    @pytest.mark.django_db
    def test_create_account_name_already_exists(self, snapshot):
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.account_storage.get_account_by_name.return_value = type(
            "Account", (), {"is_active": True, "owner_id": owner_id})

        with pytest.raises(AccountNameAlreadyExistsException) as exc:
            self.interactor.create_account(
                name="Sample Account",
                description="Sample Account description",
                created_by=owner_id)

        snapshot.assert_match(
            repr(exc.value),
            "create_account_name_already_exists.txt"
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

        self.account_storage.deactivate_account.return_value = None

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
