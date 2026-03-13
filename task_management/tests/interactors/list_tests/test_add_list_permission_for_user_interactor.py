from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    InvalidPermission,
    UserAlreadyHasListPermission,
    UserNotListMember,
)
from task_management.exceptions.enums import PermissionType, ListEntityType
from task_management.interactors.dtos import (
    CreateListPermissionDTO,
    ListDTO,
    UserListPermissionDTO,
)
from task_management.interactors.lists.create_list_permission_interactor import (
    CreateListPermissionInteractor,
)
from task_management.interactors.storage_interfaces import ListStorageInterface


class InvalidPermission:
    value = "INVALID"


def make_list() -> ListDTO:
    return ListDTO(
        list_id="list_1",
        name="List",
        description="Desc",
        is_deleted=False,
        order=1,
        is_private=True,
        created_by="user_1",
        entity_type=ListEntityType.SPACE,
        entity_id="space_1",
    )


def make_user_permission(
        permission_type=PermissionType.FULL_EDIT,
        user_id="admin") -> UserListPermissionDTO:
    return UserListPermissionDTO(
        id=1,
        list_id="list_1",
        permission_type=permission_type,
        user_id=user_id,
        is_active=True,
        added_by="owner_1",
    )


class TestAddListPermissionForUserInteractor:
    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)

        self.interactor = CreateListPermissionInteractor(
            list_storage=self.list_storage,
        )

    def _setup_dependencies(
            self, actor_permission_type=PermissionType.FULL_EDIT):
        self.list_storage.get_list.return_value = make_list()
        self.list_storage.get_user_permission_for_list.side_effect = [
            None,
            make_user_permission(permission_type=actor_permission_type),
        ]
        self.list_storage.create_list_users_permission.return_value = [
            make_user_permission(user_id="user_1")
        ]

    def test_add_list_permission_success(self):
        self._setup_dependencies()
        dto = CreateListPermissionDTO(
            list_id="list_1",
            user_id="user_1",
            permission_type=PermissionType.FULL_EDIT,
            added_by="admin",
        )

        result = self.interactor.create_list_permission(
            list_permission_dto=dto
        )

        assert result.user_id == "user_1"

    def test_add_list_permission_actor_not_member(self):
        self._setup_dependencies()
        self.list_storage.get_user_permission_for_list.side_effect = [None,
                                                                      None]
        dto = CreateListPermissionDTO(
            list_id="list_1",
            user_id="user_1",
            permission_type=PermissionType.FULL_EDIT,
            added_by="admin",
        )

        with pytest.raises(UserNotListMember):
            self.interactor.create_list_permission(
                list_permission_dto=dto)

    def test_add_list_permission_permission_denied(self):
        self._setup_dependencies(actor_permission_type=PermissionType.VIEW)
        dto = CreateListPermissionDTO(
            list_id="list_1",
            user_id="user_1",
            permission_type=PermissionType.FULL_EDIT,
            added_by="admin",
        )

        with pytest.raises(ModificationNotAllowed):
            self.interactor.create_list_permission(
                list_permission_dto=dto)

    def test_add_list_permission_duplicate(self):
        self.list_storage.get_list.return_value = make_list()
        self.list_storage.get_user_permission_for_list.return_value = (
            make_user_permission(user_id="user_1")
        )
        dto = CreateListPermissionDTO(
            list_id="list_1",
            user_id="user_1",
            permission_type=PermissionType.FULL_EDIT,
            added_by="admin",
        )

        with pytest.raises(UserAlreadyHasListPermission):
            self.interactor.create_list_permission(
                list_permission_dto=dto)

    def test_add_list_permission_invalid_permission(self):
        self._setup_dependencies()
        dto = CreateListPermissionDTO(
            list_id="list_1",
            user_id="user_1",
            permission_type=InvalidPermission,
            added_by="admin",
        )

        with pytest.raises(InvalidPermission):
            self.interactor.create_list_permission(
                list_permission_dto=dto)
