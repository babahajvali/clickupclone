import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.list_interactors.list_interactors import ListInteractor
from task_management.interactors.storage_interface.list_storage_interface import ListStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import TaskStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import FolderStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import SpaceStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import PermissionStorageInterface
from task_management.exceptions.custom_exceptions import (
    NotAccessToModificationException,
    ListNotFoundException,
    InactiveListFoundException,
)


class TestSetListPrivate:

    def setup_method(self):
        self.interactor = ListInteractor(
            list_storage=create_autospec(ListStorageInterface),
            task_storage=create_autospec(TaskStorageInterface),
            folder_storage=create_autospec(FolderStorageInterface),
            space_storage=create_autospec(SpaceStorageInterface),
            permission_storage=create_autospec(PermissionStorageInterface),
        )

    def test_set_list_private_success(self, snapshot):
        self.interactor.permission_storage.get_user_access_permissions.return_value = (
            PermissionsEnum.ADMIN.value
        )
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()

        result = self.interactor.set_list_private("list_1", "user_1")

        self.interactor.list_storage.make_list_private.assert_called_once_with("list_1")

    def test_permission_denied(self, snapshot):
        self.interactor.permission_storage.get_user_access_permissions.return_value = (
            PermissionsEnum.GUEST.value
        )

        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.set_list_private("list_1", "user_1")

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_list_not_found(self, snapshot):
        self.interactor.permission_storage.get_user_access_permissions.return_value = (
            PermissionsEnum.ADMIN.value
        )
        self.interactor.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFoundException) as exc:
            self.interactor.set_list_private("list_1", "user_1")

        snapshot.assert_match(repr(exc.value), "list_not_found.txt")

    def test_list_inactive(self, snapshot):
        self.interactor.permission_storage.get_user_access_permissions.return_value = (
            PermissionsEnum.ADMIN.value
        )
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": False}
        )()

        with pytest.raises(InactiveListFoundException) as exc:
            self.interactor.set_list_private("list_1", "user_1")

        snapshot.assert_match(repr(exc.value), "list_inactive.txt")
