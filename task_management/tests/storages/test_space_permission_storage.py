import pytest

from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import CreateUserSpacePermissionDTO
from task_management.storages.space_storage import SpaceStorage
from task_management.tests.factories.storage_factory import \
    SpaceFactory, UserFactory


class TestSpacePermissionStorage:

    @pytest.mark.django_db
    def test_create_user_space_permissions_success(self, snapshot):
        # Arrange
        space_id_1 = "12345678-1234-5678-1234-567812345678"
        space_id_2 = "12345678-1234-5678-1234-567812345679"
        user_id_1 = "12345678-1234-5678-1234-567812345680"
        user_id_2 = "12345678-1234-5678-1234-567812345681"
        added_by_id = "12345678-1234-5678-1234-567812345682"
        SpaceFactory(space_id=space_id_1)
        SpaceFactory(space_id=space_id_2)
        UserFactory(user_id=user_id_1)
        UserFactory(user_id=user_id_2)
        UserFactory(user_id=added_by_id)
        permission_data = [
            CreateUserSpacePermissionDTO(
                space_id=str(space_id_1),
                user_id=str(user_id_1),
                permission_type=PermissionType.VIEW,
                added_by=str(added_by_id)
            ),
            CreateUserSpacePermissionDTO(
                space_id=str(space_id_1),
                user_id=str(user_id_2),
                permission_type=PermissionType.FULL_EDIT,
                added_by=str(added_by_id)
            ),
            CreateUserSpacePermissionDTO(
                space_id=str(space_id_2),
                user_id=str(user_id_1),
                permission_type=PermissionType.FULL_EDIT,
                added_by=str(added_by_id)
            )
        ]
        storage = SpaceStorage()

        # Act
        result = storage.create_user_space_permissions(
            permission_data=permission_data)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_create_user_space_permissions_success.txt")

    @pytest.mark.django_db
    def test_create_user_space_permissions_single_record(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345680"
        added_by_id = "12345678-1234-5678-1234-567812345682"
        SpaceFactory(space_id=space_id)
        UserFactory(user_id=user_id)
        UserFactory(user_id=added_by_id)
        permission_data = [
            CreateUserSpacePermissionDTO(
                space_id=str(space_id),
                user_id=str(user_id),
                permission_type=PermissionType.VIEW,
                added_by=str(added_by_id)
            )
        ]
        storage = SpaceStorage()

        # Act
        result = storage.create_user_space_permissions(
            permission_data=permission_data)

        # Assert
        snapshot.assert_match(repr(result),
                              "test_create_user_space_permissions_single_record.txt")
