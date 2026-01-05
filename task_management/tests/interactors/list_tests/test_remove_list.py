import pytest
from unittest.mock import create_autospec

from faker import Faker

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserListPermissionDTO
from task_management.interactors.list_interactors.list_interactors import ListInteractor
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import ListStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import TaskStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import FolderStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import SpaceStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import SpacePermissionStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import ListPermissionStorageInterface
from task_management.interactors.storage_interface.folder_permission_storage_interface import FolderPermissionStorageInterface
from task_management.exceptions.custom_exceptions import (
    NotAccessToModificationException,
    ListNotFoundException,
    InactiveListFoundException,
)
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface

Faker.seed(0)

def make_permission(permission_type: PermissionsEnum):
    return UserListPermissionDTO(
        id=1,
        list_id="list_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )

class TestRemoveList:

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.task_storage = create_autospec(TaskStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)

        self.list_permission_storage = create_autospec(
            ListPermissionStorageInterface)
        self.folder_permission_storage = create_autospec(
            FolderPermissionStorageInterface)
        self.space_permission_storage = create_autospec(
            SpacePermissionStorageInterface)
        self.template_storage = create_autospec(TemplateStorageInterface)
        self.field_storage = create_autospec(FieldStorageInterface)

        self.interactor = ListInteractor(
            list_storage=self.list_storage,
            task_storage=self.task_storage,
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            list_permission_storage=self.list_permission_storage,
            folder_permission_storage=self.folder_permission_storage,
            space_permission_storage=self.space_permission_storage,
            template_storage=self.template_storage,
            field_storage=self.field_storage
        )

    def test_remove_list_success(self, snapshot):
        self.list_permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()

        result = self.interactor.remove_list("list_1", "user_1")

        self.interactor.list_storage.remove_list.assert_called_once_with(
            list_id="list_1"
        )

    def test_permission_denied(self, snapshot):
        self.list_permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.VIEW)
        )

        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.remove_list("list_1", "user_1")

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_list_not_found(self, snapshot):
        self.list_permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )
        self.interactor.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFoundException) as exc:
            self.interactor.remove_list("list_1", "user_1")

        snapshot.assert_match(repr(exc.value), "list_not_found.txt")

    def test_list_inactive(self, snapshot):
        self.list_permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": False}
        )()

        with pytest.raises(InactiveListFoundException) as exc:
            self.interactor.remove_list("list_1", "user_1")

        snapshot.assert_match(repr(exc.value), "list_inactive.txt")
