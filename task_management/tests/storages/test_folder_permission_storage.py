import pytest

from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import CreateFolderPermissionDTO
from task_management.storages.folder_storage import \
    FolderStorage
from task_management.tests.factories.storage_factory import \
    FolderFactory, UserFactory


class TestFolderPermissionStorage:

    @pytest.mark.django_db
    def test_create_folder_users_permissions_success(self, snapshot):
        # Arrange
        folder_id_1 = "12345678-1234-5678-1234-567812345678"
        folder_id_2 = "12345678-1234-5678-1234-567812345679"
        user_id_1 = "12345678-1234-5678-1234-567812345680"
        user_id_2 = "12345678-1234-5678-1234-567812345681"
        added_by_id = "12345678-1234-5678-1234-567812345682"
        FolderFactory(folder_id=folder_id_1)
        FolderFactory(folder_id=folder_id_2)
        UserFactory(user_id=user_id_1)
        UserFactory(user_id=user_id_2)
        UserFactory(user_id=added_by_id)
        users_permission_data = [
            CreateFolderPermissionDTO(
                folder_id=str(folder_id_1),
                user_id=str(user_id_1),
                permission_type=PermissionType.VIEW,
                added_by=str(added_by_id)
            ),
            CreateFolderPermissionDTO(
                folder_id=str(folder_id_1),
                user_id=str(user_id_2),
                permission_type=PermissionType.FULL_EDIT,
                added_by=str(added_by_id)
            ),
            CreateFolderPermissionDTO(
                folder_id=str(folder_id_2),
                user_id=str(user_id_1),
                permission_type=PermissionType.FULL_EDIT,
                added_by=str(added_by_id)
            )
        ]
        storage = FolderStorage()

        # Act
        result = storage.create_folder_users_permissions(
            users_permission_data=users_permission_data)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_create_folder_users_permissions_success.txt")

    @pytest.mark.django_db
    def test_create_folder_users_permissions_single_record(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345680"
        added_by_id = "12345678-1234-5678-1234-567812345682"
        FolderFactory(folder_id=folder_id)
        UserFactory(user_id=user_id)
        UserFactory(user_id=added_by_id)
        users_permission_data = [
            CreateFolderPermissionDTO(
                folder_id=str(folder_id),
                user_id=str(user_id),
                permission_type=PermissionType.VIEW,
                added_by=str(added_by_id)
            )
        ]
        storage = FolderStorage()

        # Act
        result = storage.create_folder_users_permissions(
            users_permission_data=users_permission_data)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_create_folder_users_permissions_single_record.txt")
