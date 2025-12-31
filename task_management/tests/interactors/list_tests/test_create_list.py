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
    SpaceNotFoundException,
    InactiveSpaceFoundException, FolderListOrderAlreadyExistedException,
)
from task_management.tests.factories.interactor_factory import CreateListDTOFactory


class TestCreateList:

    def setup_method(self):
        self.interactor = ListInteractor(
            list_storage=create_autospec(ListStorageInterface),
            task_storage=create_autospec(TaskStorageInterface),
            folder_storage=create_autospec(FolderStorageInterface),
            space_storage=create_autospec(SpaceStorageInterface),
            permission_storage=create_autospec(PermissionStorageInterface),
        )

    def test_create_list_success(self, snapshot):
        dto = CreateListDTOFactory(folder_id="!234")

        self.interactor.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.interactor.space_storage.get_space.return_value = type("Space", (), {"is_active": True})()
        self.interactor.list_storage.check_list_order_exist_in_folder.return_value = False
        self.interactor.list_storage.crate_list.return_value = "LIST_DTO"

        result = self.interactor.create_list(dto)

        snapshot.assert_match(repr(result), "create_list_success.json")

    def test_permission_denied(self, snapshot):
        dto = CreateListDTOFactory()
        self.interactor.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.GUEST.value

        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.create_list(dto)

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_space_not_found(self, snapshot):
        dto = CreateListDTOFactory()
        self.interactor.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.interactor.space_storage.get_space.return_value = None

        with pytest.raises(SpaceNotFoundException) as exc:
            self.interactor.create_list(dto)

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_space_inactive(self, snapshot):
        dto = CreateListDTOFactory()
        self.interactor.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.interactor.space_storage.get_space.return_value = type("Space", (), {"is_active": False})()

        with pytest.raises(InactiveSpaceFoundException) as exc:
            self.interactor.create_list(dto)

        snapshot.assert_match(repr(exc.value), "space_inactive.txt")

    def test_order_already_exists_in_folder(self, snapshot):
        dto = CreateListDTOFactory(folder_id= "123")
        self.interactor.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.interactor.space_storage.get_space.return_value = type("Space", (), {"is_active": True})()
        self.interactor.list_storage.check_list_order_exist_in_folder.return_value = True

        with pytest.raises(FolderListOrderAlreadyExistedException) as exc:
            self.interactor.create_list(dto)

        snapshot.assert_match(repr(exc.value), "order_already_exists.txt")
