import pytest
from unittest.mock import create_autospec

from task_management.interactors.storage_interfaces.account_storage_interface import \
    AccountStorageInterface

from task_management.interactors.workspaces.workspace_interactor import (
    WorkspaceInteractor
)
from task_management.interactors.storage_interfaces.workspace_storage_interface import (
    WorkspaceStorageInterface
)
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    UserNotFound,
    WorkspaceNotFound
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

        self.interactor = WorkspaceInteractor(
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
            account_storage=self.account_storage,
        )

    def _mock_active_user(self):
        return type("User", (), {"is_active": True})()

    def _mock_active_workspace(self, owner_id):
        return type(
            "Workspace",
            (),
            {
                "workspace_id": "workspaces-123",
                "user_id": owner_id,
                "account_id": "accounts-123",
                "is_active": True,
            }
        )()

    def test_create_workspace_success(self, snapshot):
        create_data = CreateWorkspaceFactory()
        expected = WorkspaceDTOFactory()

        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.create_workspace.return_value = expected

        self.account_storage.get_account_by_id.return_value = type(
            "Account",
            (),
            {"is_active": True,
             "owner_id": create_data.user_id}
        )()


        result = self.interactor.create_workspace(create_data)

        snapshot.assert_match(repr(result), "create_workspace_success.txt")


    def test_update_workspace_success(self, snapshot):
        update_data = WorkspaceDTOFactory()
        expected = WorkspaceDTOFactory()

        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.get_active_workspaces.return_value = \
            self._mock_active_workspace(update_data.user_id)
        self.workspace_storage.update_workspace.return_value = expected

        result = self.interactor.update_workspace(update_data,
                                                  user_id="user_id")

        snapshot.assert_match(
            repr(result),
            "update_workspace_success.txt"
        )

    def test_update_workspace_not_found(self, snapshot):
        update_data = WorkspaceDTOFactory()

        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.get_active_workspaces.return_value = None

        with pytest.raises(WorkspaceNotFound) as exc:
            self.interactor.update_workspace(update_data, user_id="user_id")

        snapshot.assert_match(
            repr(exc.value),
            "update_workspace_not_found.txt"
        )

    def test_delete_workspace_success(self, snapshot):
        workspace_id = "workspaces-123"
        user_id = "owner-123"
        expected = WorkspaceDTOFactory()

        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.get_active_workspaces.return_value = \
            self._mock_active_workspace(user_id)
        self.workspace_storage.delete_workspace.return_value = expected

        result = self.interactor.delete_workspace(workspace_id, user_id)

        snapshot.assert_match(
            repr(result),
            "delete_workspace_success.txt"
        )

    def test_transfer_workspace_success(self, snapshot):
        workspace_id = "workspaces-123"
        user_id = "owner-123"
        new_user_id = "new-owner-123"
        expected = WorkspaceDTOFactory()

        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.workspace_storage.get_active_workspaces.return_value = \
            self._mock_active_workspace(user_id)
        self.workspace_storage.transfer_workspace.return_value = expected

        result = self.interactor.transfer_workspace(
            workspace_id=workspace_id,
            user_id=user_id,
            new_user_id=new_user_id
        )

        snapshot.assert_match(
            repr(result),
            "transfer_workspace_success.txt"
        )

    def test_transfer_workspace_new_user_not_found(self, snapshot):
        workspace_id = "workspaces-123"
        user_id = "owner-123"
        new_user_id = "invalid-user"

        self.user_storage.get_user_data.side_effect = [None]
        self.workspace_storage.get_active_workspaces.return_value = \
            self._mock_active_workspace(user_id)

        with pytest.raises(UserNotFound) as exc:
            self.interactor.transfer_workspace(
                workspace_id,
                user_id,
                new_user_id
            )

        snapshot.assert_match(
            repr(exc.value),
            "transfer_workspace_user_not_found.txt"
        )
