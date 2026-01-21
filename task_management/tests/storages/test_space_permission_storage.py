import pytest

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import CreateUserSpacePermissionDTO
from task_management.storages.space_permission_storage import SpacePermissionStorage
from task_management.tests.factories.storage_factory import SpacePermissionFactory, SpaceFactory, UserFactory


class TestSpacePermissionStorage:

    @pytest.mark.django_db
    def test_get_user_permission_for_space_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        space = SpaceFactory(space_id=space_id)
        added_by = UserFactory()
        SpacePermissionFactory(user=user, space=space, added_by=added_by, permission_type="view")
        storage = SpacePermissionStorage()

        # Act
        result = storage.get_user_permission_for_space(user_id=str(user_id), space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_permission_for_space_success.txt")

    @pytest.mark.django_db
    def test_get_user_permission_for_space_failure(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        storage = SpacePermissionStorage()

        # Act
        result = storage.get_user_permission_for_space(user_id=str(user_id), space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_permission_for_space_failure.txt")

    @pytest.mark.django_db
    def test_update_user_permission_for_space_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        space = SpaceFactory(space_id=space_id)
        added_by = UserFactory()
        SpacePermissionFactory(user=user, space=space, added_by=added_by, permission_type="view")
        storage = SpacePermissionStorage()

        # Act
        result = storage.update_user_permission_for_space(
            user_id=str(user_id),
            space_id=str(space_id),
            permission_type=PermissionsEnum.FULL_EDIT
        )

        # Assert
        snapshot.assert_match(repr(result), "test_update_user_permission_for_space_success.txt")

    @pytest.mark.django_db
    def test_remove_user_permission_for_space_success(self, snapshot):
        # Arrange
        user_id = "12345678-1234-5678-1234-567812345678"
        space_id = "12345678-1234-5678-1234-567812345679"
        user = UserFactory(user_id=user_id)
        space = SpaceFactory(space_id=space_id)
        added_by = UserFactory()
        SpacePermissionFactory(user=user, space=space, added_by=added_by, is_active=True)
        storage = SpacePermissionStorage()

        # Act
        result = storage.remove_user_permission_for_space(user_id=str(user_id), space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result), "test_remove_user_permission_for_space_success.txt")

    @pytest.mark.django_db
    def test_get_space_permissions_success(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345679"
        space = SpaceFactory(space_id=space_id)
        user1 = UserFactory()
        user2 = UserFactory()
        added_by = UserFactory()
        SpacePermissionFactory(user=user1, space=space, added_by=added_by, permission_type="view", is_active=True)
        SpacePermissionFactory(user=user2, space=space, added_by=added_by, permission_type="edit", is_active=True)
        SpacePermissionFactory(user=user1, space=space, added_by=added_by, permission_type="admin", is_active=False)
        storage = SpacePermissionStorage()

        # Act
        result = storage.get_space_permissions(space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_space_permissions_success.txt")

    @pytest.mark.django_db
    def test_get_space_permissions_empty(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345679"
        SpaceFactory(space_id=space_id)
        storage = SpacePermissionStorage()

        # Act
        result = storage.get_space_permissions(space_id=str(space_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_space_permissions_empty.txt")

    @pytest.mark.django_db
    def test_create_user_space_permissions_success(self, snapshot):
        # Arrange
        space_id_1 = "12345678-1234-5678-1234-567812345678"
        space_id_2 = "12345678-1234-5678-1234-567812345679"
        user_id_1 = "12345678-1234-5678-1234-567812345680"
        user_id_2 = "12345678-1234-5678-1234-567812345681"
        added_by_id = "12345678-1234-5678-1234-567812345682"
        space1 = SpaceFactory(space_id=space_id_1)
        space2 = SpaceFactory(space_id=space_id_2)
        user1 = UserFactory(user_id=user_id_1)
        user2 = UserFactory(user_id=user_id_2)
        added_by = UserFactory(user_id=added_by_id)
        permission_data = [
            CreateUserSpacePermissionDTO(
                space_id=str(space_id_1),
                user_id=str(user_id_1),
                permission_type=PermissionsEnum.VIEW,
                added_by=str(added_by_id)
            ),
            CreateUserSpacePermissionDTO(
                space_id=str(space_id_1),
                user_id=str(user_id_2),
                permission_type=PermissionsEnum.FULL_EDIT,
                added_by=str(added_by_id)
            ),
            CreateUserSpacePermissionDTO(
                space_id=str(space_id_2),
                user_id=str(user_id_1),
                permission_type=PermissionsEnum.FULL_EDIT,
                added_by=str(added_by_id)
            )
        ]
        storage = SpacePermissionStorage()

        # Act
        result = storage.create_user_space_permissions(permission_data=permission_data)

        # Assert
        snapshot.assert_match(repr(result), "test_create_user_space_permissions_success.txt")

    @pytest.mark.django_db
    def test_create_user_space_permissions_single_record(self, snapshot):
        # Arrange
        space_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345680"
        added_by_id = "12345678-1234-5678-1234-567812345682"
        space = SpaceFactory(space_id=space_id)
        user = UserFactory(user_id=user_id)
        added_by = UserFactory(user_id=added_by_id)
        permission_data = [
            CreateUserSpacePermissionDTO(
                space_id=str(space_id),
                user_id=str(user_id),
                permission_type=PermissionsEnum.VIEW,
                added_by=str(added_by_id)
            )
        ]
        storage = SpacePermissionStorage()

        # Act
        result = storage.create_user_space_permissions(permission_data=permission_data)

        # Assert
        snapshot.assert_match(repr(result), "test_create_user_space_permissions_single_record.txt")