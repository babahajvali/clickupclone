import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserFolderPermissionDTO, \
    UserSpacePermissionDTO
from task_management.interactors.list_interactors.list_interactors import ListInteractor
from task_management.interactors.storage_interface.list_storage_interface import ListStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import TaskStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import FolderStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import SpaceStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import (
    SpacePermissionStorageInterface
)
from task_management.interactors.storage_interface.list_permission_storage_interface import (
    ListPermissionStorageInterface
)
from task_management.interactors.storage_interface.folder_permission_storage_interface import (
    FolderPermissionStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    NotAccessToModificationException,
    SpaceNotFoundException,
    InactiveSpaceFoundException,
    FolderListOrderAlreadyExistedException,
)
from task_management.tests.factories.interactor_factory import CreateListDTOFactory


def make_folder_permission(permission_type: PermissionsEnum):
    return UserFolderPermissionDTO(
        id=1,
        folder_id="folder_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )

def make_permission(permission_type: PermissionsEnum):
    return UserSpacePermissionDTO(
        id=1,
        space_id="space_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )

class TestCreateList:

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.task_storage = create_autospec(TaskStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)

        self.list_permission_storage = create_autospec(ListPermissionStorageInterface)
        self.folder_permission_storage = create_autospec(FolderPermissionStorageInterface)
        self.space_permission_storage = create_autospec(SpacePermissionStorageInterface)

        self.interactor = ListInteractor(
            list_storage=self.list_storage,
            task_storage=self.task_storage,
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            list_permission_storage=self.list_permission_storage,
            folder_permission_storage=self.folder_permission_storage,
            space_permission_storage=self.space_permission_storage,
        )

    def test_create_list_success(self, snapshot):
        dto = CreateListDTOFactory(folder_id="folder_123")

        self.folder_permission_storage.get_user_permission_for_folder.return_value = make_folder_permission(
            PermissionsEnum.FULL_EDIT
        )
        self.list_storage.check_list_order_exist_in_folder.return_value = False
        self.list_storage.create_list.return_value = "LIST_DTO"

        result = self.interactor.create_list(dto)

        snapshot.assert_match(repr(result), "create_list_success.json")

    def test_permission_denied(self, snapshot):
        dto = CreateListDTOFactory(folder_id=None)

        self.space_permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.VIEW
        )

        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.create_list(dto)

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_space_not_found(self, snapshot):
        dto = CreateListDTOFactory(folder_id=None)

        self.space_permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT
        )
        self.space_storage.get_space.return_value = None
        self.list_storage.check_list_order_exist_in_space.return_value = False

        with pytest.raises(SpaceNotFoundException) as exc:
            self.interactor.create_list(dto)

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_space_inactive(self, snapshot):
        dto = CreateListDTOFactory(folder_id=None)

        self.space_permission_storage.get_user_permission_for_space.return_value = make_permission(
            PermissionsEnum.FULL_EDIT
        )

        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": False}
        )()
        self.list_storage.check_list_order_exist_in_space.return_value = False

        with pytest.raises(InactiveSpaceFoundException) as exc:
            self.interactor.create_list(dto)

        snapshot.assert_match(repr(exc.value), "space_inactive.txt")

    def test_order_already_exists_in_folder(self, snapshot):
        dto = CreateListDTOFactory(folder_id="folder_123")

        self.folder_permission_storage.get_user_permission_for_folder.return_value = make_folder_permission(
            PermissionsEnum.FULL_EDIT
        )
        self.list_storage.check_list_order_exist_in_folder.return_value = True

        with pytest.raises(FolderListOrderAlreadyExistedException) as exc:
            self.interactor.create_list(dto)

        snapshot.assert_match(repr(exc.value), "order_already_exists.txt")
