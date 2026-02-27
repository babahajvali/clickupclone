from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    UnsupportedVisibilityType,
)
from task_management.exceptions.enums import Role, Visibility
from task_management.interactors.dtos import FolderDTO, WorkspaceMemberDTO
from task_management.interactors.folders.set_folder_visibility_interactor import (
    SetFolderVisibilityInteractor,
)
from task_management.interactors.storage_interfaces import (
    FolderStorageInterface,
    WorkspaceStorageInterface,
)


class InvalidVisibility:
    value = "INVALID"


def make_permission(role: Role) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        user_id="user_1",
        role=role,
        is_active=True,
        added_by="admin",
    )


def make_folder() -> FolderDTO:
    return FolderDTO(
        folder_id="folder_1",
        name="Folder",
        description="Desc",
        space_id="space_1",
        order=1,
        is_deleted=False,
        created_by="user_1",
        is_private=False,
    )


class TestSetFolderVisibilityInteractor:
    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = SetFolderVisibilityInteractor(
            folder_storage=self.folder_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER):
        self.folder_storage.get_folder.return_value = make_folder()
        self.folder_storage.get_workspace_id_from_folder_id.return_value = (
            "workspace_1"
        )
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )
        self.folder_storage.update_folder_visibility.return_value = make_folder()

    def test_set_folder_visibility_success(self, snapshot):
        self._setup_dependencies()

        result = self.interactor.set_folder_visibility(
            folder_id="folder_1",
            user_id="user_1",
            visibility=Visibility.PRIVATE,
        )

        snapshot.assert_match(repr(result), "set_folder_visibility_success.txt")

    def test_set_folder_visibility_invalid_type(self, snapshot):
        self._setup_dependencies()

        with pytest.raises(UnsupportedVisibilityType) as exc:
            self.interactor.set_folder_visibility(
                folder_id="folder_1",
                user_id="user_1",
                visibility=InvalidVisibility,
            )

        snapshot.assert_match(
            repr(exc.value), "set_folder_visibility_invalid_type.txt"
        )

    def test_set_folder_visibility_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.set_folder_visibility(
                folder_id="folder_1",
                user_id="user_1",
                visibility=Visibility.PRIVATE,
            )

        snapshot.assert_match(
            repr(exc.value), "set_folder_visibility_permission_denied.txt"
        )
