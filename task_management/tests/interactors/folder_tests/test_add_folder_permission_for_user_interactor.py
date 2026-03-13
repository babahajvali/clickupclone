from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import \
    ModificationNotAllowed, \
    InvalidPermission as InvalidPermissionException, UserNotFolderMember
from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import (
    CreateFolderPermissionDTO,
    FolderDTO,
    UserFolderPermissionDTO,
)
from task_management.interactors.folders.create_folder_permission_interactor import (
    CreateFolderPermissionInteractor,
)
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface


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
        permission_type=PermissionType.FULL_EDIT,
        user_id="user_1",
        is_active=True,
        added_by="admin",
    )


def make_editor_permission(permission_type=PermissionType.FULL_EDIT):
    return UserFolderPermissionDTO(
        id=9,
        folder_id="folder_1",
        permission_type=permission_type,
        user_id="admin",
        is_active=True,
        added_by="owner_1",
    )


class InvalidPermissionValue:
    value = "INVALID"


class TestAddFolderPermissionForUserInteractor:
    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)

        self.interactor = CreateFolderPermissionInteractor(
            folder_storage=self.folder_storage,
        )

    def _setup_dependencies(
            self, permission_type=PermissionType.FULL_EDIT):
        self.folder_storage.get_folder.return_value = make_folder()
        self.folder_storage.get_user_folder_permission.return_value = (
            make_editor_permission(permission_type=permission_type)
        )
        self.folder_storage.create_folder_users_permissions.return_value = [
            make_user_permission()
        ]

    def test_add_folder_permission_success(self, snapshot):
        self._setup_dependencies()
        dto = CreateFolderPermissionDTO(
            folder_id="folder_1",
            user_id="user_1",
            permission_type=PermissionType.FULL_EDIT,
            added_by="admin",
        )

        result = self.interactor.create_folder_permission(
            create_folder_permission_dto=dto
        )

        snapshot.assert_match(repr(result),
                              "add_folder_permission_success.txt")

    def test_add_folder_permission_permission_denied(self, snapshot):
        self._setup_dependencies(permission_type=PermissionType.VIEW)
        dto = CreateFolderPermissionDTO(
            folder_id="folder_1",
            user_id="user_1",
            permission_type=PermissionType.FULL_EDIT,
            added_by="admin",
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_folder_permission(
                create_folder_permission_dto=dto)

        snapshot.assert_match(
            repr(exc.value), "add_folder_permission_permission_denied.txt"
        )

    def test_add_folder_permission_actor_not_member(self, snapshot):
        self._setup_dependencies()
        self.folder_storage.get_user_folder_permission.return_value = None
        dto = CreateFolderPermissionDTO(
            folder_id="folder_1",
            user_id="user_1",
            permission_type=PermissionType.FULL_EDIT,
            added_by="admin",
        )

        with pytest.raises(UserNotFolderMember) as exc:
            self.interactor.create_folder_permission(
                create_folder_permission_dto=dto)

        snapshot.assert_match(
            repr(exc.value), "add_folder_permission_actor_not_member.txt"
        )

    def test_add_folder_permission_unexpected_permission(self):
        self._setup_dependencies()
        dto = CreateFolderPermissionDTO(
            folder_id="folder_1",
            user_id="user_1",
            permission_type=InvalidPermissionValue,
            added_by="admin",
        )

        with pytest.raises(InvalidPermissionException) as exc:
            self.interactor.create_folder_permission(
                create_folder_permission_dto=dto)

        assert repr(exc.value) == "InvalidPermission()"
