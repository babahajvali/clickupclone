import pytest

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import CreateUserListPermissionDTO
from task_management.storages.list_permission_storage import ListPermissionStorage
from task_management.tests.factories.storage_factory import ListPermissionFactory, ListFactory, UserFactory


class TestListPermissionStorage:

    @pytest.mark.django_db
    def test_update_user_permission_for_list_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        added_by = UserFactory()
        ListPermissionFactory(list=list_obj, user=user, added_by=added_by, permission_type="view")
        storage = ListPermissionStorage()

        # Act
        result = storage.update_user_permission_for_list(
            list_id=str(list_id),
            user_id=str(user_id),
            permission_type=PermissionsEnum.FULL_EDIT
        )

        # Assert
        snapshot.assert_match(repr(result), "test_update_user_permission_for_list_success.txt")

    @pytest.mark.django_db
    def test_get_list_permissions_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        list_obj = ListFactory(list_id=list_id)
        user1 = UserFactory()
        user2 = UserFactory()
        added_by = UserFactory()
        ListPermissionFactory(list=list_obj, user=user1, added_by=added_by, permission_type="view")
        ListPermissionFactory(list=list_obj, user=user2, added_by=added_by, permission_type="edit")
        storage = ListPermissionStorage()

        # Act
        result = storage.get_list_permissions(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_list_permissions_success.txt")

    @pytest.mark.django_db
    def test_get_list_permissions_empty(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        ListFactory(list_id=list_id)
        storage = ListPermissionStorage()

        # Act
        result = storage.get_list_permissions(list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_list_permissions_empty.txt")

    @pytest.mark.django_db
    def test_get_user_permission_for_list_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        added_by = UserFactory()
        ListPermissionFactory(list=list_obj, user=user, added_by=added_by, permission_type="view")
        storage = ListPermissionStorage()

        # Act
        result = storage.get_user_permission_for_list(user_id=str(user_id), list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_permission_for_list_success.txt")

    @pytest.mark.django_db
    def test_get_user_permission_for_list_failure(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        storage = ListPermissionStorage()

        # Act
        result = storage.get_user_permission_for_list(user_id=str(user_id), list_id=str(list_id))

        # Assert
        snapshot.assert_match(repr(result), "test_get_user_permission_for_list_failure.txt")

    @pytest.mark.django_db
    def test_remove_user_permission_for_list_success(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345679"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        added_by = UserFactory()
        ListPermissionFactory(list=list_obj, user=user, added_by=added_by, is_active=True)
        storage = ListPermissionStorage()

        # Act
        result = storage.remove_user_permission_for_list(list_id=str(list_id), user_id=str(user_id))

        # Assert
        snapshot.assert_match(repr(result), "test_remove_user_permission_for_list_success.txt")

    @pytest.mark.django_db
    def test_create_list_users_permissions_success(self, snapshot):
        # Arrange
        list_id_1 = "12345678-1234-5678-1234-567812345678"
        list_id_2 = "12345678-1234-5678-1234-567812345679"
        user_id_1 = "12345678-1234-5678-1234-567812345680"
        user_id_2 = "12345678-1234-5678-1234-567812345681"
        added_by_id = "12345678-1234-5678-1234-567812345682"
        list1 = ListFactory(list_id=list_id_1)
        list2 = ListFactory(list_id=list_id_2)
        user1 = UserFactory(user_id=user_id_1)
        user2 = UserFactory(user_id=user_id_2)
        added_by = UserFactory(user_id=added_by_id)
        user_permissions = [
            CreateUserListPermissionDTO(
                list_id=str(list_id_1),
                user_id=str(user_id_1),
                permission_type=PermissionsEnum.VIEW,
                added_by=str(added_by_id)
            ),
            CreateUserListPermissionDTO(
                list_id=str(list_id_1),
                user_id=str(user_id_2),
                permission_type=PermissionsEnum.FULL_EDIT,
                added_by=str(added_by_id)
            ),
            CreateUserListPermissionDTO(
                list_id=str(list_id_2),
                user_id=str(user_id_1),
                permission_type=PermissionsEnum.FULL_EDIT,
                added_by=str(added_by_id)
            )
        ]
        storage = ListPermissionStorage()

        # Act
        result = storage.create_list_users_permissions(user_permissions=user_permissions)

        # Assert
        snapshot.assert_match(repr(result), "test_create_list_users_permissions_success.txt")

    @pytest.mark.django_db
    def test_create_list_users_permissions_single_record(self, snapshot):
        # Arrange
        list_id = "12345678-1234-5678-1234-567812345678"
        user_id = "12345678-1234-5678-1234-567812345680"
        added_by_id = "12345678-1234-5678-1234-567812345682"
        list_obj = ListFactory(list_id=list_id)
        user = UserFactory(user_id=user_id)
        added_by = UserFactory(user_id=added_by_id)
        user_permissions = [
            CreateUserListPermissionDTO(
                list_id=str(list_id),
                user_id=str(user_id),
                permission_type=PermissionsEnum.VIEW,
                added_by=str(added_by_id)
            )
        ]
        storage = ListPermissionStorage()

        # Act
        result = storage.create_list_users_permissions(user_permissions=user_permissions)

        # Assert
        snapshot.assert_match(repr(result), "test_create_list_users_permissions_single_record.txt")