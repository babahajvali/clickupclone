from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    FolderNotFound,
    ModificationNotAllowed,
    NothingToUpdateFolderException,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import FolderDTO, WorkspaceMemberDTO
from task_management.interactors.folders.update_folder_interactor import (
    UpdateFolderInteractor,
)
from task_management.interactors.storage_interfaces import (
    FolderStorageInterface,
    SpaceStorageInterface,
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


def make_folder(order: int = 1) -> FolderDTO:
    return FolderDTO(
        folder_id="folder_1",
        name="Folder",
        description="Desc",
        space_id="space_1",
        order=order,
        is_deleted=False,
        created_by="user_1",
        is_private=False,
    )


class TestUpdateFolderInteractor:
    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = UpdateFolderInteractor(
            folder_storage=self.folder_storage,
            workspace_storage=self.workspace_storage,
            space_storage=self.space_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER):
        self.folder_storage.get_folder.return_value = make_folder()
        self.folder_storage.get_folder_space_id.return_value = "space_1"
        self.space_storage.get_space_workspace_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )
        self.folder_storage.update_folder.return_value = make_folder()

    def test_update_folder_success(self, snapshot):
        self._setup_dependencies()

        result = self.interactor.update_folder(
            folder_id="folder_1",
            user_id="user_1",
            name="Updated",
            description="Updated Desc",
        )

        snapshot.assert_match(repr(result), "update_folder_success.txt")

    def test_update_folder_nothing_to_update(self, snapshot):
        self._setup_dependencies()

        with pytest.raises(NothingToUpdateFolderException) as exc:
            self.interactor.update_folder(
                folder_id="folder_1",
                user_id="user_1",
                name=None,
                description=None,
            )

        snapshot.assert_match(
            repr(exc.value), "update_folder_nothing_to_update.txt"
        )

    def test_update_folder_not_found(self, snapshot):
        self._setup_dependencies()
        self.folder_storage.get_folder.return_value = None

        with pytest.raises(FolderNotFound) as exc:
            self.interactor.update_folder(
                folder_id="folder_1",
                user_id="user_1",
                name="Updated",
                description=None,
            )

        snapshot.assert_match(repr(exc.value), "update_folder_not_found.txt")

    def test_update_folder_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.update_folder(
                folder_id="folder_1",
                user_id="user_1",
                name="Updated",
                description=None,
            )

        snapshot.assert_match(
            repr(exc.value), "update_folder_permission_denied.txt"
        )
