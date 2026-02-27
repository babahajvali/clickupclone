from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    FolderNotFound,
    ModificationNotAllowed,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import FolderDTO, WorkspaceMemberDTO
from task_management.interactors.folders.delete_folder_interactor import (
    DeleteFolderInteractor,
)
from task_management.interactors.storage_interfaces import (
    FolderStorageInterface,
    WorkspaceStorageInterface,
)


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


class TestDeleteFolderInteractor:
    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = DeleteFolderInteractor(
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
        self.folder_storage.delete_folder.return_value = make_folder()

    def test_delete_folder_success(self, snapshot):
        self._setup_dependencies()

        result = self.interactor.delete_folder(
            folder_id="folder_1", user_id="user_1"
        )

        snapshot.assert_match(repr(result), "delete_folder_success.txt")

    def test_delete_folder_not_found(self, snapshot):
        self._setup_dependencies()
        self.folder_storage.get_folder.return_value = None

        with pytest.raises(FolderNotFound) as exc:
            self.interactor.delete_folder(folder_id="folder_1", user_id="user_1")

        snapshot.assert_match(repr(exc.value), "delete_folder_not_found.txt")

    def test_delete_folder_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.delete_folder(folder_id="folder_1", user_id="user_1")

        snapshot.assert_match(
            repr(exc.value), "delete_folder_permission_denied.txt"
        )
