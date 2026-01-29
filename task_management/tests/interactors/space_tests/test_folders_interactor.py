import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import PermissionsEnum, Visibility
from task_management.interactors.dtos import UserSpacePermissionDTO, \
    UserFolderPermissionDTO
from task_management.interactors.space_interactors.folders_interactor import FolderInteractor
from task_management.interactors.storage_interface.folder_storage_interface import FolderStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import SpaceStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import (
    SpacePermissionStorageInterface
)
from task_management.interactors.storage_interface.folder_permission_storage_interface import (
    FolderPermissionStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowedException,
    InactiveSpaceException,
    FolderNotFoundException,
    InactiveFolderException,
)
from task_management.tests.factories.interactor_factory import (
    CreateFolderDTOFactory,
    UpdateFolderDTOFactory,
    FolderDTOFactory,
)

def make_permission(permission_type: PermissionsEnum):
    return UserSpacePermissionDTO(
        id=1,
        space_id="space_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )

def make_folder_permission(permission_type: PermissionsEnum):
    return UserFolderPermissionDTO(
        id=1,
        folder_id="folder_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )

class TestFolderInteractor:

    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.space_permission_storage = create_autospec(SpacePermissionStorageInterface)
        self.folder_permission_storage = create_autospec(FolderPermissionStorageInterface)

        self.interactor = FolderInteractor(
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            space_permission_storage=self.space_permission_storage,
            folder_permission_storage=self.folder_permission_storage,
        )

    def test_create_folder_success(self, snapshot):
        dto = CreateFolderDTOFactory()
        expected = FolderDTOFactory()

        self.space_permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT.value
        )
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": True}
        )()
        self.folder_storage.create_folder.return_value = expected

        result = self.interactor.create_folder(dto)

        snapshot.assert_match(
            repr(result),
            "create_folder_success.txt"
        )

    def test_create_folder_permission_denied(self, snapshot):
        dto = CreateFolderDTOFactory()

        self.space_permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.VIEW.value
        )

        with pytest.raises(ModificationNotAllowedException) as exc:
            self.interactor.create_folder(dto)

        snapshot.assert_match(
            repr(exc.value.user_id),
            "create_folder_permission_denied.txt"
        )

    def test_create_folder_inactive_space(self, snapshot):
        dto = CreateFolderDTOFactory()

        self.space_permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT.value
        )
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": False}
        )()

        with pytest.raises(InactiveSpaceException) as exc:
            self.interactor.create_folder(dto)

        snapshot.assert_match(
            repr(exc.value.space_id),
            "create_folder_inactive_space.txt"
        )


    def test_update_folder_success(self, snapshot):
        dto = UpdateFolderDTOFactory()
        expected = FolderDTOFactory()

        self.folder_permission_storage.get_user_permission_for_folder.return_value = make_folder_permission(
            PermissionsEnum.FULL_EDIT.value
        )
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": True,
                           "space_id":"space_id",}
        )()
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": True}
        )()
        self.folder_storage.update_folder.return_value = expected

        result = self.interactor.update_folder(dto,user_id="user_id1")

        snapshot.assert_match(
            repr(result),
            "update_folder_success.txt"
        )

    def test_update_folder_permission_denied(self, snapshot):
        dto = UpdateFolderDTOFactory()

        self.folder_permission_storage.get_user_permission_for_folder.return_value = make_folder_permission(
            PermissionsEnum.VIEW.value
        )

        with pytest.raises(ModificationNotAllowedException) as exc:
            self.interactor.update_folder(dto,user_id="user_id1")

        snapshot.assert_match(
            repr(exc.value.user_id),
            "update_folder_permission_denied.txt"
        )

    def test_update_folder_not_found(self, snapshot):
        dto = UpdateFolderDTOFactory()

        self.folder_permission_storage.get_user_permission_for_folder.return_value = make_folder_permission(
            PermissionsEnum.FULL_EDIT.value
        )
        self.folder_storage.get_folder.return_value = None

        with pytest.raises(FolderNotFoundException) as exc:
            self.interactor.update_folder(dto,user_id="user_id1")

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "update_folder_not_found.txt"
        )


    def test_remove_folder_success(self, snapshot):
        folder_id = "folder_1"
        user_id = "user_1"
        expected = FolderDTOFactory(is_active=False)

        self.folder_permission_storage.get_user_permission_for_folder.return_value = make_folder_permission(
            PermissionsEnum.FULL_EDIT.value
        )
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": True}
        )()
        self.folder_storage.remove_folder.return_value = expected

        result = self.interactor.remove_folder(folder_id, user_id)

        snapshot.assert_match(
            repr(result),
            "remove_folder_success.txt"
        )

    def test_remove_folder_not_found(self, snapshot):
        folder_id = "folder_1"
        user_id = "user_1"

        self.folder_permission_storage.get_user_permission_for_folder.return_value = make_folder_permission(
            PermissionsEnum.FULL_EDIT.value
        )
        self.folder_storage.get_folder.return_value = None

        with pytest.raises(FolderNotFoundException) as exc:
            self.interactor.remove_folder(folder_id, user_id)

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "remove_folder_not_found.txt"
        )

    def test_remove_folder_inactive(self, snapshot):
        folder_id = "folder_1"
        user_id = "user_1"

        self.folder_permission_storage.get_user_permission_for_folder.return_value = make_folder_permission(
            PermissionsEnum.FULL_EDIT.value
        )
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": False}
        )()

        with pytest.raises(InactiveFolderException) as exc:
            self.interactor.remove_folder(folder_id, user_id)

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "remove_folder_inactive.txt"
        )


    def test_make_folder_private_success(self, snapshot):
        folder_id = "folder_1"
        user_id = "user_1"
        expected = FolderDTOFactory(is_private=True)

        self.folder_permission_storage.get_user_permission_for_folder.return_value = make_folder_permission(
            PermissionsEnum.FULL_EDIT.value
        )
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": True}
        )()
        self.folder_storage.set_folder_private.return_value = expected

        result = self.interactor.set_folder_visibility(folder_id, user_id,Visibility.PRIVATE)

        snapshot.assert_match(
            repr(result),
            "make_folder_private_success.txt"
        )

    def test_make_folder_public_inactive(self, snapshot):
        folder_id = "folder_1"
        user_id = "user_1"

        self.folder_permission_storage.get_user_permission_for_folder.return_value = make_folder_permission(
            PermissionsEnum.FULL_EDIT.value
        )
        self.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": False}
        )()

        with pytest.raises(InactiveFolderException) as exc:
            self.interactor.set_folder_visibility(folder_id, user_id,Visibility.PUBLIC)

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "make_folder_public_inactive.txt"
        )
