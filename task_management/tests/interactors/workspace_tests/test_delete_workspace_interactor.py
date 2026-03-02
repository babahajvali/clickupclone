from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    UserNotWorkspaceOwner,
    WorkspaceNotFound,
)
from task_management.interactors.dtos import WorkspaceDTO
from task_management.interactors.storage_interfaces import WorkspaceStorageInterface
from task_management.interactors.workspaces.delete_workspace_interactor import (
    DeleteWorkspaceInteractor,
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


class TestDeleteWorkspaceInteractor:
    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = DeleteWorkspaceInteractor(
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, is_owner: bool = True):
        self.workspace_storage.get_workspace.return_value = make_workspace()
        self.workspace_storage.validate_user_is_workspace_owner.return_value = is_owner
        self.workspace_storage.delete_workspace.return_value = make_workspace()

    def test_delete_workspace_success(self, snapshot):
        self._setup_dependencies()

        result = self.interactor.delete_workspace(
            workspace_id="workspace_1",
            user_id="user_1",
        )

        snapshot.assert_match(repr(result), "delete_workspace_success.txt")

    def test_delete_workspace_not_found(self, snapshot):
        self._setup_dependencies()
        self.workspace_storage.get_workspace.return_value = None

        with pytest.raises(WorkspaceNotFound) as exc:
            self.interactor.delete_workspace(
                workspace_id="workspace_1",
                user_id="user_1",
            )

        snapshot.assert_match(repr(exc.value), "delete_workspace_not_found.txt")

    def test_delete_workspace_permission_denied(self, snapshot):
        self._setup_dependencies(is_owner=False)

        with pytest.raises(UserNotWorkspaceOwner) as exc:
            self.interactor.delete_workspace(
                workspace_id="workspace_1",
                user_id="user_1",
            )

        snapshot.assert_match(
            repr(exc.value),
            "delete_workspace_permission_denied.txt",
        )
