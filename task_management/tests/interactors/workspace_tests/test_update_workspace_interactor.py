from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    NothingToUpdateWorkspace,
    UserNotWorkspaceOwner,
    WorkspaceNotFound,
)
from task_management.interactors.dtos import WorkspaceDTO
from task_management.interactors.storage_interfaces import WorkspaceStorageInterface
from task_management.interactors.workspaces.update_workspace_interactor import (
    UpdateWorkspaceInteractor,
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


class TestUpdateWorkspaceInteractor:
    def setup_method(self):
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = UpdateWorkspaceInteractor(
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, is_owner: bool = True):
        self.workspace_storage.get_workspace.return_value = make_workspace()
        self.workspace_storage.validate_user_is_workspace_owner.return_value = is_owner
        self.workspace_storage.update_workspace.return_value = WorkspaceDTO(
            workspace_id="workspace_1",
            name="Updated Workspace",
            description="Updated Description",
            user_id="user_1",
            account_id="account_1",
            is_deleted=False,
        )

    def test_update_workspace_success(self, snapshot):
        self._setup_dependencies()

        result = self.interactor.update_workspace(
            workspace_id="workspace_1",
            user_id="user_1",
            name="Updated Workspace",
            description="Updated Description",
        )

        snapshot.assert_match(repr(result), "update_workspace_success.txt")

    def test_update_workspace_nothing_to_update(self, snapshot):
        with pytest.raises(NothingToUpdateWorkspace) as exc:
            self.interactor.update_workspace(
                workspace_id="workspace_1",
                user_id="user_1",
                name=None,
                description=None,
            )

        snapshot.assert_match(
            repr(exc.value), "update_workspace_nothing_to_update.txt"
        )

    def test_update_workspace_not_found(self, snapshot):
        self._setup_dependencies()
        self.workspace_storage.get_workspace.return_value = None

        with pytest.raises(WorkspaceNotFound) as exc:
            self.interactor.update_workspace(
                workspace_id="workspace_1",
                user_id="user_1",
                name="Updated Workspace",
                description=None,
            )

        snapshot.assert_match(repr(exc.value), "update_workspace_not_found.txt")

    def test_update_workspace_permission_denied(self, snapshot):
        self._setup_dependencies(is_owner=False)

        with pytest.raises(UserNotWorkspaceOwner) as exc:
            self.interactor.update_workspace(
                workspace_id="workspace_1",
                user_id="user_1",
                name="Updated Workspace",
                description=None,
            )

        snapshot.assert_match(
            repr(exc.value), "update_workspace_permission_denied.txt"
        )
