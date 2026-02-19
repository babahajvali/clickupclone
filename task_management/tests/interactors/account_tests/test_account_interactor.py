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
    AccountNameAlreadyExistsException, UserNotAccountOwnerException,
    EmptyNameException, UserNotFoundException, InactiveUserException,
    AccountNotFoundException, InactiveAccountException,
    NothingToUpdateAccountException, InvalidAccountIdsException
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

    def _mock_account(self, owner_id, is_active=True):
        return type(
            "Account",
            (),
            {"owner_id": owner_id, "is_active": is_active}
        )()

    # ------------------------------------------------------------------ #
    #  create_account
    # ------------------------------------------------------------------ #

    def test_create_account_success(self, snapshot):
        expected = AccountDTOFactory()
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.account_storage.get_account_by_name.return_value = False
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

    def test_empty_account_name_exists(self, snapshot):
        owner_id = "12345678-1234-5678-1234-567812345678"
        self.account_storage.get_account_by_name.return_value = None
        account_name = ""

        with pytest.raises(EmptyNameException) as exc:
            self.interactor.create_account(
                name=account_name,
                description="Sample Account description",
                created_by=owner_id
            )

        snapshot.assert_match(repr(exc.value),
                              "create_empty_account_name_exists.txt")

    def test_create_account_whitespace_name(self, snapshot):
        owner_id = "12345678-1234-5678-1234-567812345678"

        with pytest.raises(EmptyNameException) as exc:
            self.interactor.create_account(
                name="   ",
                description="desc",
                created_by=owner_id
            )

        snapshot.assert_match(repr(exc.value),
                              "create_account_whitespace_name.txt")

    def test_create_account_non_owner(self, snapshot):
        owner_id = "some-other-user"

        self.user_storage.get_user_data.return_value = None

        with pytest.raises(UserNotFoundException) as exc:
            self.interactor.create_account(
                name="Sample Account",
                description="Sample Account description",
                created_by=owner_id
            )

        snapshot.assert_match(repr(exc.value), 'create_account_non_owner.txt')

    def test_create_account_inactive_user(self, snapshot):
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.user_storage.get_user_data.return_value = type('user', (), {
            "is_active": False})()

        with pytest.raises(InactiveUserException) as e:
            self.interactor.create_account(
                name="Sample Account",
                description="Sample Account description",
                created_by=owner_id
            )

        snapshot.assert_match(repr(e.value),
                              'create_account_inactive_user.txt')

    def test_create_account_with_no_description(self, snapshot):
        """description is optional – passing None should succeed."""
        expected = AccountDTOFactory()
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.account_storage.get_account_by_name.return_value = False
        self.account_storage.create_account.return_value = expected

        result = self.interactor.create_account(
            name="No Desc Account",
            description=None,
            created_by=owner_id
        )

        snapshot.assert_match(repr(result),
                              "create_account_no_description.txt")

    # ------------------------------------------------------------------ #
    #  update_account
    # ------------------------------------------------------------------ #

    def test_update_account_name_success(self, snapshot):
        from django.core.exceptions import ObjectDoesNotExist

        account_id = "account-123"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id)
        self.account_storage.get_account_by_name.side_effect = ObjectDoesNotExist
        expected = AccountDTOFactory()
        self.account_storage.update_account.return_value = expected

        result = self.interactor.update_account(
            account_id=account_id,
            user_id=owner_id,
            name="New Name",
            description=None
        )

        snapshot.assert_match(repr(result), "update_account_name_success.txt")

    def test_update_account_description_success(self, snapshot):
        account_id = "account-123"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id)
        expected = AccountDTOFactory()
        self.account_storage.update_account.return_value = expected

        result = self.interactor.update_account(
            account_id=account_id,
            user_id=owner_id,
            name=None,
            description="Updated description"
        )

        snapshot.assert_match(repr(result),
                              "update_account_description_success.txt")

    def test_update_account_both_fields_success(self, snapshot):
        from django.core.exceptions import ObjectDoesNotExist

        account_id = "account-123"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id)
        self.account_storage.get_account_by_name.side_effect = ObjectDoesNotExist
        expected = AccountDTOFactory()
        self.account_storage.update_account.return_value = expected

        result = self.interactor.update_account(
            account_id=account_id,
            user_id=owner_id,
            name="New Name",
            description="New Description"
        )

        snapshot.assert_match(repr(result),
                              "update_account_both_fields_success.txt")

    def test_update_account_nothing_to_update(self, snapshot):
        account_id = "account-123"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id)

        with pytest.raises(NothingToUpdateAccountException) as exc:
            self.interactor.update_account(
                account_id=account_id,
                user_id=owner_id,
                name=None,
                description=None
            )

        snapshot.assert_match(repr(exc.value),
                              "update_account_nothing_to_update.txt")

    def test_update_account_name_already_exists(self, snapshot):
        account_id = "account-123"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id)
        # Returns a *different* account with the same name
        self.account_storage.get_account_by_name.return_value = "different-account-id"

        with pytest.raises(AccountNameAlreadyExistsException) as exc:
            self.interactor.update_account(
                account_id=account_id,
                user_id=owner_id,
                name="Taken Name",
                description=None
            )

        snapshot.assert_match(repr(exc.value),
                              "update_account_name_already_exists.txt")

    def test_update_account_non_owner(self, snapshot):
        account_id = "account-123"
        owner_id = "actual-owner"
        other_user = "intruder-user"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id)

        with pytest.raises(UserNotAccountOwnerException) as exc:
            self.interactor.update_account(
                account_id=account_id,
                user_id=other_user,
                name="New Name",
                description=None
            )

        snapshot.assert_match(repr(exc.value),
                              "update_account_non_owner.txt")

    def test_update_account_not_found(self, snapshot):
        account_id = "non-existent-account"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = None

        with pytest.raises(AccountNotFoundException) as exc:
            self.interactor.update_account(
                account_id=account_id,
                user_id=owner_id,
                name="Name",
                description=None
            )

        snapshot.assert_match(repr(exc.value),
                              "update_account_not_found.txt")

    def test_update_account_inactive(self, snapshot):
        account_id = "account-123"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id, is_active=False)

        with pytest.raises(InactiveAccountException) as exc:
            self.interactor.update_account(
                account_id=account_id,
                user_id=owner_id,
                name="New Name",
                description=None
            )

        snapshot.assert_match(repr(exc.value),
                              "update_account_inactive.txt")

    # ------------------------------------------------------------------ #
    #  delete_account
    # ------------------------------------------------------------------ #

    def test_delete_account_success(self, snapshot):
        account_id = "account-123"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id)

        result = self.interactor.delete_account(
            account_id=account_id,
            deleted_by=owner_id
        )

        snapshot.assert_match(
            repr(result),
            "delete_account_success.txt"
        )

    def test_account_not_found(self, snapshot):
        account_id = "account-123"
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.account_storage.get_account_by_id.return_value = None
        with pytest.raises(AccountNotFoundException) as e:
            self.interactor.delete_account(account_id=account_id,
                                           deleted_by=owner_id)

        snapshot.assert_match(repr(e.value), 'account_not_found.txt')

    def test_inactive_account_exists(self, snapshot):
        account_id = "account-123"
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.account_storage.get_account_by_id.return_value = type(
            'account', (), {'is_active': False})()

        with pytest.raises(InactiveAccountException) as e:
            self.interactor.delete_account(account_id=account_id,
                                           deleted_by=owner_id)

        snapshot.assert_match(repr(e.value), 'inactive_account_exists.txt')

    def test_delete_account_non_owner(self, snapshot):
        account_id = "account-123"
        user_id = "user-999"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            "some-other-user")

        with pytest.raises(UserNotAccountOwnerException) as exc:
            self.interactor.delete_account(
                account_id=account_id,
                deleted_by=user_id
            )

        snapshot.assert_match(
            repr(exc.value),
            "delete_account_non_owner.txt"
        )

    # ------------------------------------------------------------------ #
    #  deactivate_account
    # ------------------------------------------------------------------ #

    def test_deactivate_account_success(self, snapshot):
        account_id = "account-123"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id)

        result = self.interactor.deactivate_account(
            account_id=account_id,
            deactivated_by=owner_id
        )

        snapshot.assert_match(repr(result), "deactivate_account_success.txt")

    def test_deactivate_account_not_found(self, snapshot):
        account_id = "non-existent"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = None

        with pytest.raises(AccountNotFoundException) as exc:
            self.interactor.deactivate_account(
                account_id=account_id,
                deactivated_by=owner_id
            )

        snapshot.assert_match(repr(exc.value),
                              "deactivate_account_not_found.txt")

    def test_deactivate_account_already_inactive(self, snapshot):
        account_id = "account-123"
        owner_id = "user-123"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id, is_active=False)

        with pytest.raises(InactiveAccountException) as exc:
            self.interactor.deactivate_account(
                account_id=account_id,
                deactivated_by=owner_id
            )

        snapshot.assert_match(repr(exc.value),
                              "deactivate_account_already_inactive.txt")

    def test_deactivate_account_non_owner(self, snapshot):
        account_id = "account-123"
        owner_id = "actual-owner"
        other_user = "intruder"

        self.account_storage.get_account_by_id.return_value = self._mock_account(
            owner_id)

        with pytest.raises(UserNotAccountOwnerException) as exc:
            self.interactor.deactivate_account(
                account_id=account_id,
                deactivated_by=other_user
            )

        snapshot.assert_match(repr(exc.value),
                              "deactivate_account_non_owner.txt")

    # ------------------------------------------------------------------ #
    #  get_accounts
    # ------------------------------------------------------------------ #

    def test_get_accounts_success(self, snapshot):
        account_id1 = "12345678-1234-5678-1234-567812345678"
        account_id2 = "12345678-1234-5678-1234-567812345679"

        accounts_data = [
            AccountDTOFactory(account_id=account_id1),
            AccountDTOFactory(account_id=account_id2),
        ]
        self.account_storage.get_accounts.return_value = accounts_data

        result = self.interactor.get_accounts(
            account_ids=[account_id1, account_id2],
        )

        snapshot.assert_match(repr(result), 'get_accounts_success.txt')

    def test_get_accounts_invalid_ids(self, snapshot):
        valid_id = "12345678-1234-5678-1234-567812345678"
        invalid_id = "invalid-id-999"

        # Storage returns only the valid account
        mock_account = type("Account", (), {
            "account_id": valid_id, "is_active": True})()
        self.account_storage.get_accounts.return_value = [mock_account]

        with pytest.raises(InvalidAccountIdsException) as exc:
            self.interactor.get_accounts(
                account_ids=[valid_id, invalid_id]
            )

        snapshot.assert_match(repr(exc.value),
                              "get_accounts_invalid_ids.txt")

    def test_get_accounts_empty_list(self, snapshot):
        self.account_storage.get_accounts.return_value = []

        result = self.interactor.get_accounts(account_ids=[])

        snapshot.assert_match(repr(result), "get_accounts_empty_list.txt")