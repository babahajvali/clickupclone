import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.space_interactors.folders_interactor import FolderInteractor
from task_management.interactors.storage_interface.folder_storage_interface import FolderStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import SpaceStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import PermissionStorageInterface
from task_management.exceptions.custom_exceptions import (
    NotAccessToModificationException,
    SpaceNotFoundException,
    InactiveSpaceFoundException,
    FolderNotFoundException,
    InactiveFolderFoundException
)
from task_management.tests.factories.interactor_factory import (
    CreateFolderDTOFactory,
    UpdateFolderDTOFactory,
    FolderDTOFactory
)


class TestFolderInteractor:

    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.permission_storage = create_autospec(PermissionStorageInterface)
        
        self.interactor = FolderInteractor(
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            permission_storage=self.permission_storage
        )

    def test_create_folder_success(self, snapshot):
        # Arrange
        create_data = CreateFolderDTOFactory()
        expected_result = FolderDTOFactory()
        
        # Mock dependencies
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.space_storage.get_space.return_value = type('Space', (), {'is_active': True})()
        self.folder_storage.check_order_exist.return_value = False
        self.folder_storage.create_folder.return_value = expected_result

        # Act
        result = self.interactor.create_folder(create_data)

        # Assert
        assert result == expected_result
        self.folder_storage.create_folder.assert_called_once_with(create_data)

    def test_create_folder_permission_denied(self, snapshot):
        # Arrange
        create_data = CreateFolderDTOFactory()
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.GUEST.value

        # Act & Assert
        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.create_folder(create_data)

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_create_folder_space_not_found(self, snapshot):
        # Arrange
        create_data = CreateFolderDTOFactory()
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.space_storage.get_space.return_value = None

        # Act & Assert
        with pytest.raises(SpaceNotFoundException) as exc:
            self.interactor.create_folder(create_data)

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_create_folder_space_inactive(self, snapshot):
        # Arrange
        create_data = CreateFolderDTOFactory()
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.space_storage.get_space.return_value = type('Space', (), {'is_active': False})()

        # Act & Assert
        with pytest.raises(InactiveSpaceFoundException) as exc:
            self.interactor.create_folder(create_data)

        snapshot.assert_match(repr(exc.value), "space_inactive.txt")

    def test_update_folder_success(self):
        # Arrange
        update_data = UpdateFolderDTOFactory()
        expected_result = FolderDTOFactory()
        
        # Mock dependencies
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.space_storage.get_space.return_value = type('Space', (), {'is_active': True})()
        self.folder_storage.get_folder.return_value = type('Folder', (), {'is_active': True})()
        self.folder_storage.check_order_exist.return_value = False
        self.folder_storage.update_folder.return_value = expected_result

        # Act
        result = self.interactor.update_folder(update_data)

        # Assert
        assert result == expected_result
        self.folder_storage.update_folder.assert_called_once_with(update_data)

    def test_remove_folder_success(self):
        # Arrange
        folder_id = "folder123"
        user_id = "user123"
        expected_result = FolderDTOFactory()
        
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.folder_storage.get_folder.return_value = type('Folder', (), {'is_active': True})()
        self.folder_storage.remove_folder.return_value = expected_result

        # Act
        result = self.interactor.remove_folder(folder_id, user_id)

        # Assert
        assert result == expected_result
        self.folder_storage.remove_folder.assert_called_once_with(folder_id)

    def test_make_folder_private_success(self):
        # Arrange
        folder_id = "folder123"
        user_id = "user123"
        expected_result = FolderDTOFactory()
        
        # Mock dependencies
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.folder_storage.get_folder.return_value = type('Folder', (), {'is_active': True})()
        self.folder_storage.set_folder_private.return_value = expected_result

        # Act
        result = self.interactor.make_folder_private(folder_id, user_id)

        # Assert
        assert result == expected_result
        self.folder_storage.set_folder_private.assert_called_once_with(folder_id)

    def test_make_folder_public_success(self):
        # Arrange
        folder_id = "folder123"
        user_id = "user123"
        expected_result = FolderDTOFactory()
        
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.folder_storage.get_folder.return_value = type('Folder', (), {'is_active': True})()
        self.folder_storage.set_folder_public.return_value = expected_result

        # Act
        result = self.interactor.make_folder_public(folder_id, user_id)

        # Assert
        assert result == expected_result
        self.folder_storage.set_folder_public.assert_called_once_with(folder_id)

    def test_get_space_folders_success(self):
        # Arrange
        space_id = "space123"
        expected_folders = [FolderDTOFactory() for _ in range(3)]
        
        # Mock dependencies
        self.space_storage.get_space.return_value = type('Space', (), {'is_active': True})()
        self.folder_storage.get_space_folders.return_value = expected_folders

        # Act
        result = self.interactor.get_space_folders(space_id)

        # Assert
        assert result == expected_folders
        self.folder_storage.get_space_folders.assert_called_once_with(space_id)

    def test_get_space_folders_space_not_found(self, snapshot):
        # Arrange
        space_id = "nonexistent_space"
        self.space_storage.get_space.return_value = None

        # Act & Assert
        with pytest.raises(SpaceNotFoundException) as exc:
            self.interactor.get_space_folders(space_id)

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_get_space_folders_space_inactive(self, snapshot):
        # Arrange
        space_id = "inactive_space"
        self.space_storage.get_space.return_value = type('Space', (), {'is_active': False})()

        # Act & Assert
        with pytest.raises(InactiveSpaceFoundException) as exc:
            self.interactor.get_space_folders(space_id)

        snapshot.assert_match(repr(exc.value), "space_inactive.txt")
