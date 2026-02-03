import pytest
from unittest.mock import create_autospec, MagicMock


from task_management.interactors.storage_interface.account_storage_interface import \
    AccountStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.workspace_interactors.workspace_interactors import (
    WorkspaceInteractor
)
from task_management.interactors.storage_interface.workspace_storage_interface import (
    WorkspaceStorageInterface
)
from task_management.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    UserNotFoundException,
    WorkspaceNotFoundException
)
from task_management.tests.factories.interactor_factory import (
    CreateWorkspaceFactory,
    WorkspaceDTOFactory
)


class TestWorkspaceInteractor:

    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.account_storage = create_autospec(AccountStorageInterface)
        self.workspace_member_storage = create_autospec(WorkspaceMemberStorageInterface)

        self.interactor = WorkspaceInteractor(
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
            account_storage=self.account_storage,
            workspace_member_storage=self.workspace_member_storage
        )


    def _mock_active_user(self):
        return type("User", (), {"is_active": True})()

    def _mock_active_workspace(self, owner_id):
        return type(
            "Workspace",
            (),
            {"owner_id": owner_id, "is_active": True}
        )()


    def test_create_workspace_success(self, snapshot):
        create_data = CreateWorkspaceFactory()
        expected = WorkspaceDTOFactory()

        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.create_workspace.return_value = expected

        permission = type("Account")()
        self.account_storage.get_account_by_id.return_value = permission

        result = self.interactor.create_workspace(create_data)

        snapshot.assert_match(repr(result),"create_workspace_success.txt")

    def test_create_workspace_user_not_found(self, snapshot):
        create_data = CreateWorkspaceFactory()

        self.user_storage.get_user_data.return_value = None

        with pytest.raises(UserNotFoundException) as exc:
            self.interactor.create_workspace(create_data)

        snapshot.assert_match(
            repr(exc.value),
            "create_workspace_user_not_found.txt"
        )

    def test_update_workspace_success(self, snapshot):
        update_data = WorkspaceDTOFactory()
        expected = WorkspaceDTOFactory()

        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.get_workspace.return_value = \
            self._mock_active_workspace(update_data.user_id)
        self.workspace_storage.update_workspace.return_value = expected

        result = self.interactor.update_workspace(update_data,user_id="user_id")

        snapshot.assert_match(
            repr(result),
            "update_workspace_success.txt"
        )

    def test_update_workspace_not_found(self, snapshot):
        update_data = WorkspaceDTOFactory()

        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.get_workspace.return_value = None

        with pytest.raises(WorkspaceNotFoundException) as exc:
            self.interactor.update_workspace(update_data,user_id="user_id")

        snapshot.assert_match(
            repr(exc.value),
            "update_workspace_not_found.txt"
        )


    def test_delete_workspace_success(self, snapshot):
        workspace_id = "workspace-123"
        user_id = "owner-123"
        expected = WorkspaceDTOFactory()

        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.get_workspace.return_value = \
            self._mock_active_workspace(user_id)
        self.workspace_storage.delete_workspace.return_value = expected

        result = self.interactor.delete_workspace(workspace_id, user_id)

        snapshot.assert_match(
            repr(result),
            "delete_workspace_success.txt"
        )


    def test_transfer_workspace_success(self, snapshot):
        workspace_id = "workspace-123"
        user_id = "owner-123"
        new_user_id = "new-owner-123"
        expected = WorkspaceDTOFactory()

        self.user_storage.get_user_data.side_effect = [self._mock_active_user(),  # new owner
        ]
        self.workspace_storage.get_workspace.return_value = \
            self._mock_active_workspace(user_id)
        self.workspace_storage.transfer_workspace.return_value = expected

        result = self.interactor.transfer_workspace(
            workspace_id,
            user_id,
            new_user_id
        )

        snapshot.assert_match(
            repr(result),
            "transfer_workspace_success.txt"
        )

    def test_transfer_workspace_new_user_not_found(self, snapshot):
        workspace_id = "workspace-123"
        user_id = "owner-123"
        new_user_id = "invalid-user"

        self.user_storage.get_user_data.side_effect = [None]
        self.workspace_storage.get_workspace.return_value = \
            self._mock_active_workspace(user_id)

        with pytest.raises(UserNotFoundException) as exc:
            self.interactor.transfer_workspace(
                workspace_id,
                user_id,
                new_user_id
            )

        snapshot.assert_match(
            repr(exc.value),
            "transfer_workspace_user_not_found.txt"
        )
