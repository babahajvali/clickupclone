import pytest
from factory.random import reseed_random

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import CreateUserFolderPermissionDTO
from task_management.storages.folder_permission_storage import \
    FolderPermissionStorage
from task_management.tests.factories.storage_factory import \
    FolderPermissionFactory, FolderFactory, UserFactory


class TestFolderPermissionStorage:

    @pytest.mark.django_db
    def test_get_user_permission_for_folder_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        added_by_id = "12345678-1234-5678-1234-567812345680"
        user = UserFactory(user_id=user_id)
        folder = FolderFactory(folder_id=folder_id)
        added_by = UserFactory(user_id=added_by_id)
        FolderPermissionFactory(user=user, folder=folder, added_by=added_by,
                                permission_type="view")
        storage = FolderPermissionStorage()

        # Act
        result = storage.get_user_permission_for_folder(user_id=str(user_id),
                                                        folder_id=str(
                                                            folder_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_user_permission_for_folder_success.txt")

    @pytest.mark.django_db
    def test_get_user_permission_for_folder_failure(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        storage = FolderPermissionStorage()

        # Act
        result = storage.get_user_permission_for_folder(user_id=str(user_id),
                                                        folder_id=str(
                                                            folder_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_user_permission_for_folder_failure.txt")

    @pytest.mark.django_db
    def test_update_user_permission_for_folder_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        added_by_id = "12345678-1234-5678-1234-567812345680"
        user = UserFactory(user_id=user_id)
        folder = FolderFactory(folder_id=folder_id)
        added_by = UserFactory(user_id=added_by_id)
        FolderPermissionFactory(user=user, folder=folder, added_by=added_by,
                                permission_type="view")
        storage = FolderPermissionStorage()

        # Act
        result = storage.update_user_permission_for_folder(
            user_id=str(user_id),
            folder_id=str(folder_id),
            permission_type=Permissions.FULL_EDIT
        )

        # Assert
        snapshot.assert_match(repr(result),
                              "test_update_user_permission_for_folder_success.txt")

    @pytest.mark.django_db
    def test_remove_user_permission_for_folder_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        folder_id = "12345678-1234-5678-1234-567812345679"
        added_by_id = "12345678-1234-5678-1234-567812345680"
        user = UserFactory(user_id=user_id)
        folder = FolderFactory(folder_id=folder_id)
        added_by = UserFactory(user_id=added_by_id)
        FolderPermissionFactory(user=user, folder=folder, added_by=added_by,
                                is_active=True)
        storage = FolderPermissionStorage()

        # Act
        result = storage.remove_user_permission_for_folder(
            folder_id=str(folder_id), user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_remove_user_permission_for_folder_success.txt")

    @pytest.mark.django_db
    def test_get_folder_permissions_success(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345679"
        added_by_id = "12345678-1234-5678-1234-567812345680"
        folder = FolderFactory(folder_id=folder_id)
        user1 = UserFactory(user_id="12345678-1234-5678-1234-567812345681")
        user2 = UserFactory(user_id="12345678-1234-5678-1234-567812345682")
        added_by = UserFactory(user_id=added_by_id)
        FolderPermissionFactory(user=user1, folder=folder, added_by=added_by,
                                permission_type="view")
        FolderPermissionFactory(user=user2, folder=folder, added_by=added_by,
                                permission_type="edit")
        storage = FolderPermissionStorage()

        # Act
        result = storage.get_folder_permissions(folder_id=str(folder_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_folder_permissions_success.txt")

    @pytest.mark.django_db
    def test_get_folder_permissions_empty(self, snapshot):
        # Arrange
        folder_id = "12345678-1234-5678-1234-567812345679"
        FolderFactory(folder_id=folder_id)
        storage = FolderPermissionStorage()

        # Act
        result = storage.get_folder_permissions(folder_id=str(folder_id))

        # Assert
        snapshot.assert_match(repr(result),
                              "test_get_folder_permissions_empty.txt")

    @pytest.mark.django_db
    def test_create_folder_users_permissions_success(self, snapshot):
        # Arrange
        folder_id_1 = "12345678-1234-5678-1234-567812345678"
        folder_id_2 = "12345678-1234-5678-1234-567812345679"
        user_id_1 = "12345678-1234-5678-1234-567812345680"
        user_id_2 = "12345678-1234-5678-1234-567812345681"
        added_by_id = "12345678-1234-5678-1234-567812345682"
        folder1 = FolderFactory(folder_id=folder_id_1)
        folder2 = FolderFactory(folder_id=folder_id_2)
        user1 = UserFactory(user_id=user_id_1)
        user2 = UserFactory(user_id=user_id_2)
        added_by = UserFactory(user_id=added_by_id)
        users_permission_data = [
            CreateUserFolderPermissionDTO(
                folder_id=str(folder_id_1),
                user_id=str(user_id_1),
                permission_type=Permissions.VIEW,
                added_by=str(added_by_id)
            ),
            CreateUserFolderPermissionDTO(
                folder_id=str(folder_id_1),
                user_id=str(user_id_2),
                permission_type=Permissions.FULL_EDIT,
                added_by=str(added_by_id)
            ),
            CreateUserFolderPermissionDTO(
                folder_id=str(folder_id_2),
                user_id=str(user_id_1),
                permission_type=Permissions.FULL_EDIT,
                added_by=str(added_by_id)
            )
        ]
        storage = FolderPermissionStorage()

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
        folder = FolderFactory(folder_id=folder_id)
        user = UserFactory(user_id=user_id)
        added_by = UserFactory(user_id=added_by_id)
        users_permission_data = [
            CreateUserFolderPermissionDTO(
                folder_id=str(folder_id),
                user_id=str(user_id),
                permission_type=Permissions.VIEW,
                added_by=str(added_by_id)
            )
        ]
        storage = FolderPermissionStorage()

        # Act
        result = storage.create_folder_users_permissions(
            users_permission_data=users_permission_data)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_create_folder_users_permissions_single_record.txt")
