from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedWorkspaceFound,
    UserNotWorkspaceOwner,
    InactiveUser,
    UserNotFound,
)
from task_management.interactors.dtos import WorkspaceDTO
from task_management.interactors.storage_interfaces import (
    WorkspaceStorageInterface,
    UserStorageInterface,
)
from task_management.interactors.workspaces.transfer_workspace_interactor import (
    TransferWorkspaceInteractor,
)


def make_workspace(owner_id: str = "user_1") -> WorkspaceDTO:
    return WorkspaceDTO(
        workspace_id="workspace_1",
        name="Workspace",
        description="Description",
        user_id=owner_id,
        account_id="account_1",
        is_deleted=False,
    )


def make_workspace_model(owner_id="user_1", is_deleted=False):
    return type(
        "Workspace",
        (),
        {
            "workspace_id": "workspace_1",
            "user_id": owner_id,
            "is_deleted": is_deleted,
        },
    )()


def make_user(is_active: bool = True):
    return type(
        "User",
        (),
        {
            "is_active": is_active,
        },
    )()


class TestTransferWorkspaceInteractor:

    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)

        self.interactor = TransferWorkspaceInteractor(
            workspace_storage=self.workspace_storage,
            user_storage=self.user_storage,
        )

    def test_transfer_workspace_success(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            make_workspace_model(owner_id="user_1")
        )
        self.user_storage.get_user_data.return_value = make_user(True)
        self.workspace_storage.transfer_workspace.return_value = (
            make_workspace(owner_id="new_user")
        )

        result = self.interactor.transfer_workspace(
            workspace_id="workspace_1",
            user_id="user_1",
            new_user_id="new_user",
        )

        snapshot.assert_match(
            repr(result),
            "transfer_workspace_success.txt",
        )

    def test_transfer_workspace_deleted_workspace(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            make_workspace_model(is_deleted=True)
        )

        with pytest.raises(DeletedWorkspaceFound) as exc:
            self.interactor.transfer_workspace(
                workspace_id="workspace_1",
                user_id="user_1",
                new_user_id="new_user",
            )

        snapshot.assert_match(
            repr(exc.value),
            "transfer_workspace_deleted_workspace.txt",
        )

    def test_transfer_workspace_not_owner(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            make_workspace_model(is_deleted=False)
        )
        self.workspace_storage.validate_user_is_workspace_owner.return_value = False

        with pytest.raises(UserNotWorkspaceOwner) as exc:
            self.interactor.transfer_workspace(
                workspace_id="workspace_1",
                user_id="user_1",
                new_user_id="new_user",
            )

        snapshot.assert_match(
            repr(exc.value),
            "transfer_workspace_permission_denied.txt",
        )

    def test_transfer_workspace_new_user_inactive(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            make_workspace_model(owner_id="user_1")
        )
        self.user_storage.get_user_data.return_value = make_user(False)

        with pytest.raises(InactiveUser) as exc:
            self.interactor.transfer_workspace(
                workspace_id="workspace_1",
                user_id="user_1",
                new_user_id="new_user",
            )

        snapshot.assert_match(
            repr(exc.value),
            "transfer_workspace_new_user_inactive.txt",
        )

    def test_transfer_workspace_new_user_not_found(self, snapshot):
        self.workspace_storage.get_workspace.return_value = (
            make_workspace_model(owner_id="user_1")
        )
        self.user_storage.get_user_data.return_value = None

        with pytest.raises(UserNotFound) as exc:
            self.interactor.transfer_workspace(
                workspace_id="workspace_1",
                user_id="user_1",
                new_user_id="new_user",
            )

        snapshot.assert_match(
            repr(exc.value),
            "transfer_workspace_user_not_found.txt",
        )
