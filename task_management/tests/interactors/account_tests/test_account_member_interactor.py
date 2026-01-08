from unittest.mock import create_autospec

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.account_interactor.account_member_interactor import \
    AccountMemberInteractor

from task_management.interactors.storage_interface.account_member_storage_interface import (
    AccountMemberStorageInterface
)
from task_management.interactors.storage_interface.account_storage_interface import (
    AccountStorageInterface
)
from task_management.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface
)
from task_management.interactors.storage_interface.workspace_storage_interface import (
    WorkspaceStorageInterface
)
from task_management.interactors.storage_interface.workspace_member_storage_interface import (
    WorkspaceMemberStorageInterface
)
from task_management.interactors.storage_interface.space_permission_storage_interface import (
    SpacePermissionStorageInterface
)
from task_management.interactors.storage_interface.folder_permission_storage_interface import (
    FolderPermissionStorageInterface
)
from task_management.interactors.storage_interface.list_permission_storage_interface import (
    ListPermissionStorageInterface
)
from task_management.interactors.storage_interface.space_storage_interface import (
    SpaceStorageInterface
)
from task_management.interactors.storage_interface.folder_storage_interface import (
    FolderStorageInterface
)
from task_management.interactors.storage_interface.list_storage_interface import (
    ListStorageInterface
)

from task_management.tests.factories.interactor_factory import (
    CreateAccountMemberFactory,
    AccountMemberDTOFactory
)


class TestAccountMemberInteractor:

    def setup_method(self):
        self.account_member_storage = create_autospec(
            AccountMemberStorageInterface)
        self.account_storage = create_autospec(AccountStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.workspace_member_storage = create_autospec(
            WorkspaceMemberStorageInterface)
        self.space_permission_storage = create_autospec(
            SpacePermissionStorageInterface)
        self.folder_permission_storage = create_autospec(
            FolderPermissionStorageInterface)
        self.list_permission_storage = create_autospec(
            ListPermissionStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)

        self.interactor = AccountMemberInteractor(
            account_member_storage=self.account_member_storage,
            account_storage=self.account_storage,
            user_storage=self.user_storage,
            workspace_storage=self.workspace_storage,
            workspace_member_storage=self.workspace_member_storage,
            space_permission_storage=self.space_permission_storage,
            folder_permission_storage=self.folder_permission_storage,
            list_permission_storage=self.list_permission_storage,
            space_storage=self.space_storage,
            folder_storage=self.folder_storage,
            list_storage=self.list_storage
        )

    # ---------------- ADD MEMBER ---------------- #

    def test_add_member_to_account_success(self, snapshot):
        create_data = CreateAccountMemberFactory(role=Role.MEMBER)
        expected = AccountMemberDTOFactory(role=Role.MEMBER)

        # ValidationMixin dependencies
        self.account_storage.get_account_by_id.return_value = type(
            "Account", (), {"is_active": True}
        )()
        self.user_storage.get_user_data.return_value = type(
            "User", (), {"is_active": True}
        )()
        permission = type("Permission", (), {"role": Role.OWNER})()
        self.account_member_storage.get_user_permission_for_account.return_value = permission

        self.account_member_storage.add_member_to_account.return_value = expected
        self.workspace_storage.get_workspaces_by_account.return_value = []

        result = self.interactor.add_member_to_account(create_data)

        snapshot.assert_match(
            repr(result),
            "add_member_to_account_success.txt"
        )

    # ---------------- UPDATE ROLE ---------------- #

    def test_update_member_role_success(self, snapshot):
        account_member_id = 1
        changed_by = "user-123"

        existing = AccountMemberDTOFactory(role=Role.MEMBER)
        updated = AccountMemberDTOFactory(role=Role.ADMIN)

        self.account_member_storage.get_account_member_permission.return_value = existing
        permission = type("Permission", (), {"role": Role.OWNER})()
        self.account_member_storage.get_user_permission_for_account.return_value = permission

        self.account_member_storage.update_member_role.return_value = updated
        self.workspace_storage.get_workspaces_by_account.return_value = []

        result = self.interactor.update_member_role(
            account_member_id=account_member_id,
            role=Role.ADMIN,
            changed_by=changed_by
        )

        snapshot.assert_match(
            repr(result),
            "update_member_role_success.txt"
        )

    # ---------------- REMOVE MEMBER ---------------- #

    def test_remove_member_from_account_success(self, snapshot):
        account_member_id = 1
        removed_by = "owner-123"

        existing = AccountMemberDTOFactory()

        self.account_member_storage.get_account_member_permission.return_value = existing
        permission = type("Permission", (), {"role": Role.OWNER})()
        self.account_member_storage.get_user_permission_for_account.return_value = permission

        self.account_member_storage.delete_account_member_permission.return_value = existing
        self.workspace_storage.get_workspaces_by_account.return_value = []

        result = self.interactor.remove_member_from_account(
            account_member_id=account_member_id,
            removed_by=removed_by
        )

        snapshot.assert_match(
            repr(result),
            "remove_member_from_account_success.txt"
        )

    def test_add_member_to_account_no_access(self, snapshot):
        create_data = CreateAccountMemberFactory(role=Role.MEMBER)

        self.account_storage.get_account_by_id.return_value = type(
            "Account", (), {"is_active": True}
        )()

        self.user_storage.get_user_data.return_value = type(
            "User", (), {"is_active": True}
        )()

        self.account_member_storage.get_user_permission_for_account.return_value = None

        with pytest.raises(Exception) as exc:
            self.interactor.add_member_to_account(create_data)

        snapshot.assert_match(
            repr(exc.value),
            "add_member_to_account_no_access.txt"
        )

    def test_remove_member_from_account_unauthorized(self, snapshot):
        account_member_id = 1
        removed_by = "guest-user"

        existing = AccountMemberDTOFactory()

        self.account_member_storage.get_account_member_permission.return_value = existing
        self.account_member_storage.get_user_permission_for_account.return_value = \
            type("Permission", (), {"role": Role.GUEST})()

        with pytest.raises(Exception) as exc:
            self.interactor.remove_member_from_account(
                account_member_id=account_member_id,
                removed_by=removed_by
            )

        snapshot.assert_match(
            repr(exc.value),
            "remove_member_from_account_unauthorized.txt"
        )

    def test_add_member_account_inactive(self, snapshot):
        create_data = CreateAccountMemberFactory()

        self.account_storage.get_account_by_id.return_value = \
            type("Account", (), {"is_active": False})()

        with pytest.raises(Exception) as exc:
            self.interactor.add_member_to_account(create_data)

        snapshot.assert_match(
            repr(exc.value),
            "add_member_account_inactive.txt"
        )

    def test_update_member_role_not_found(self, snapshot):
        self.account_member_storage.get_account_member_permission.return_value = None

        with pytest.raises(Exception) as exc:
            self.interactor.update_member_role(
                account_member_id=99,
                role=Role.ADMIN,
                changed_by="user-1"
            )

        snapshot.assert_match(
            repr(exc.value),
            "update_member_role_not_found.txt"
        )

    def test_add_member_no_workspaces(self, snapshot):
        create_data = CreateAccountMemberFactory()
        expected = AccountMemberDTOFactory()

        self.account_storage.get_account_by_id.return_value = \
            type("Account", (), {"is_active": True})()
        self.user_storage.get_user_data.return_value = \
            type("User", (), {"is_active": True})()
        self.account_member_storage.get_user_permission_for_account.return_value = \
            type("Permission", (), {"role": Role.OWNER})()

        self.account_member_storage.add_member_to_account.return_value = expected
        self.workspace_storage.get_workspaces_by_account.return_value = []

        result = self.interactor.add_member_to_account(create_data)

        snapshot.assert_match(
            repr(result),
            "add_member_no_workspaces.txt"
        )
