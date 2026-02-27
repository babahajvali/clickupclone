from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import WorkspaceNotFound
from task_management.interactors.dtos import SpaceDTO
from task_management.interactors.spaces.get_workspace_spaces_interactor import (
    GetWorkspaceSpacesInteractor,
)
from task_management.interactors.storage_interfaces import (
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)


def make_space(order: int = 1) -> SpaceDTO:
    return SpaceDTO(
        space_id="space_1",
        name="Space",
        description="Desc",
        workspace_id="workspace_1",
        order=order,
        is_deleted=False,
        is_private=False,
        created_by="user_1",
    )


class TestGetWorkspaceSpacesInteractor:
    def setup_method(self):
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = GetWorkspaceSpacesInteractor(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_get_workspace_spaces_success(self, snapshot):
        self.workspace_storage.get_workspace.return_value = type(
            "Workspace", (), {"is_deleted": False}
        )()
        self.space_storage.get_workspace_spaces.return_value = [make_space()]

        result = self.interactor.get_workspace_spaces(workspace_id="workspace_1")

        snapshot.assert_match(repr(result), "get_workspace_spaces_success.txt")

    def test_get_workspace_spaces_workspace_not_found(self, snapshot):
        self.workspace_storage.get_workspace.return_value = None

        with pytest.raises(WorkspaceNotFound) as exc:
            self.interactor.get_workspace_spaces(workspace_id="workspace_1")

        snapshot.assert_match(
            repr(exc.value), "get_workspace_spaces_workspace_not_found.txt"
        )
