import pytest
from unittest.mock import create_autospec

from task_management.interactors.dtos import PermissionsEnum
from task_management.interactors.list_interactors.list_interactors import ListInteractor
from task_management.interactors.storage_interface.list_storage_interface import ListStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import TaskStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import FolderStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import SpaceStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import PermissionStorageInterface
from task_management.exceptions.custom_exceptions import (
    ListNotFoundException,
    InactiveListFoundException,
    NotAccessToCreationException,
    SpaceNotFoundException,
    ListOrderAlreadyExistedException,
)
from task_management.tests.factories.interactor_factory import UpdateListDTOFactory


class TestUpdateList:

    def setup_method(self):
        self.interactor = ListInteractor(
            list_storage=create_autospec(ListStorageInterface),
            task_storage=create_autospec(TaskStorageInterface),
            folder_storage=create_autospec(FolderStorageInterface),
            space_storage=create_autospec(SpaceStorageInterface),
            permission_storage=create_autospec(PermissionStorageInterface),
        )

    def test_update_list_success(self, snapshot):
        dto = UpdateListDTOFactory()

        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.interactor.permission_storage.get_user_access_permissions.return_value = (
            PermissionsEnum.ADMIN.value
        )
        self.interactor.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": True}
        )()
        self.interactor.list_storage.check_list_order_exist.return_value = False
        self.interactor.list_storage.update_list.return_value = "UPDATED_LIST_DTO"

        result = self.interactor.update_list(dto)

        snapshot.assert_match(
            repr(result),
            "update_list_success.json"
        )

    def test_list_not_found(self, snapshot):
        dto = UpdateListDTOFactory()
        self.interactor.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFoundException) as exc:
            self.interactor.update_list(dto)

        snapshot.assert_match(repr(exc.value), "list_not_found.txt")

    def test_list_inactive(self, snapshot):
        dto = UpdateListDTOFactory()
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": False}
        )()

        with pytest.raises(InactiveListFoundException) as exc:
            self.interactor.update_list(dto)

        snapshot.assert_match(repr(exc.value), "list_inactive.txt")

    def test_permission_denied(self, snapshot):
        dto = UpdateListDTOFactory()
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.interactor.permission_storage.get_user_access_permissions.return_value = (
            PermissionsEnum.GUEST.value
        )

        with pytest.raises(NotAccessToCreationException) as exc:
            self.interactor.update_list(dto)

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_space_not_found(self, snapshot):
        dto = UpdateListDTOFactory()
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.interactor.permission_storage.get_user_access_permissions.return_value = (
            PermissionsEnum.ADMIN.value
        )
        self.interactor.space_storage.get_space.return_value = None

        with pytest.raises(SpaceNotFoundException) as exc:
            self.interactor.update_list(dto)

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_order_already_exists(self, snapshot):
        dto = UpdateListDTOFactory()
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.interactor.permission_storage.get_user_access_permissions.return_value = (
            PermissionsEnum.ADMIN.value
        )
        self.interactor.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": True}
        )()
        self.interactor.list_storage.check_list_order_exist.return_value = True

        with pytest.raises(ListOrderAlreadyExistedException) as exc:
            self.interactor.update_list(dto)

        snapshot.assert_match(repr(exc.value), "order_already_exists.txt")
