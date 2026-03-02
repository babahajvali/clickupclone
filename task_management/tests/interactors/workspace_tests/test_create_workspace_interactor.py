from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    AccountNotFound,
    EmptyWorkspaceName,
    UserNotAccountOwner,
)
from task_management.interactors.dtos import CreateWorkspaceDTO, WorkspaceDTO
from task_management.interactors.storage_interfaces import (
    AccountStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.workspaces.create_workspace_interactor import (
    CreateWorkspaceInteractor,
)


def make_workspace() -> WorkspaceDTO:
    return WorkspaceDTO(
        workspace_id="workspace_1",
        name="Workspace",
        description="Description",
        user_id="user_1",
        account_id="account_1",
        is_deleted=False,
    )


def make_account(owner_id: str = "user_1", is_active: bool = True):
    return type(
        "Account",
        (),
        {
            "owner_id": owner_id,
            "is_active": is_active,
        },
    )()


class TestCreateWorkspaceInteractor:
    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.account_storage = create_autospec(AccountStorageInterface)

        self.interactor = CreateWorkspaceInteractor(
            workspace_storage=self.workspace_storage,
            account_storage=self.account_storage,
        )

    @staticmethod
    def _make_input(name: str = "Workspace") -> CreateWorkspaceDTO:
        return CreateWorkspaceDTO(
            name=name,
            description="Description",
            user_id="user_1",
            account_id="account_1",
        )

    def test_create_workspace_success(self, snapshot):
        self.account_storage.get_account.return_value = make_account()
        self.workspace_storage.create_workspace.return_value = make_workspace()
        input_data = self._make_input()

        result = self.interactor.create_workspace(workspace_data=input_data)

        snapshot.assert_match(repr(result), "create_workspace_success.txt")

    def test_create_workspace_empty_name(self, snapshot):
        input_data = self._make_input(name="   ")

        with pytest.raises(EmptyWorkspaceName) as exc:
            self.interactor.create_workspace(workspace_data=input_data)

        snapshot.assert_match(repr(exc.value),
                              "create_workspace_empty_name.txt")

    def test_create_workspace_account_not_found(self, snapshot):
        self.account_storage.get_account.return_value = None
        input_data = self._make_input()

        with pytest.raises(AccountNotFound) as exc:
            self.interactor.create_workspace(workspace_data=input_data)

        snapshot.assert_match(
            repr(exc.value),
            "create_workspace_account_not_found.txt",
        )

    def test_create_workspace_permission_denied(self, snapshot):
        self.account_storage.get_account.return_value = make_account(
            owner_id="another_user"
        )
        input_data = self._make_input()

        with pytest.raises(UserNotAccountOwner) as exc:
            self.interactor.create_workspace(workspace_data=input_data)

        snapshot.assert_match(
            repr(exc.value),
            "create_workspace_permission_denied.txt",
        )
