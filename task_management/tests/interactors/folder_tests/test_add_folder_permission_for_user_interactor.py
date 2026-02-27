from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import ModificationNotAllowed
from task_management.exceptions.enums import Permissions, Role
from task_management.interactors.dtos import (
    CreateFolderPermissionDTO,
    FolderDTO,
    UserFolderPermissionDTO,
    WorkspaceMemberDTO,
)
from task_management.interactors.folders.add_folder_permission_for_user_interactor import (
    AddFolderPermissionForUserInteractor,
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


def make_user_permission() -> UserFolderPermissionDTO:
    return UserFolderPermissionDTO(
        id=1,
        folder_id="folder_1",
        permission_type=Permissions.FULL_EDIT,
        user_id="user_1",
        is_active=True,
        added_by="admin",
    )


class TestAddFolderPermissionForUserInteractor:
    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = AddFolderPermissionForUserInteractor(
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
        self.folder_storage.create_folder_users_permissions.return_value = [
            make_user_permission()
        ]

    def test_add_folder_permission_success(self, snapshot):
        self._setup_dependencies()
        dto = CreateFolderPermissionDTO(
            folder_id="folder_1",
            user_id="user_1",
            permission_type=Permissions.FULL_EDIT,
            added_by="admin",
        )

        result = self.interactor.add_user_for_folder_permission(
            permission_data=dto
        )

        snapshot.assert_match(repr(result), "add_folder_permission_success.txt")

    def test_add_folder_permission_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)
        dto = CreateFolderPermissionDTO(
            folder_id="folder_1",
            user_id="user_1",
            permission_type=Permissions.FULL_EDIT,
            added_by="admin",
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.add_user_for_folder_permission(permission_data=dto)

        snapshot.assert_match(
            repr(exc.value), "add_folder_permission_permission_denied.txt"
        )
