import pytest
from unittest.mock import create_autospec

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
    ListNotFoundException, InactiveListFoundException, SpaceNotFoundException,
    NotAccessToModificationException, SpaceListOrderAlreadyExistedException,
    InvalidOrderException,
)
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.tests.factories.interactor_factory import UpdateListDTOFactory

def make_permission(permission_type: PermissionsEnum):
    return UserListPermissionDTO(
        id=1,
        list_id="list_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestUpdateList:

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

    def test_update_list_success(self, snapshot):
        dto = UpdateListDTOFactory(folder_id="764969664")

        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.list_permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )

        self.interactor.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": True}
        )()
        self.interactor.list_storage.check_list_order_exist_in_folder.return_value = False
        self.interactor.list_storage.get_folder_lists_count.return_value = 100
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
        self.list_permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.VIEW)
        )

        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.update_list(dto)

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_space_not_found(self, snapshot):
        dto = UpdateListDTOFactory()
        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.list_permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )
        self.interactor.space_storage.get_space.return_value = None

        with pytest.raises(SpaceNotFoundException) as exc:
            self.interactor.update_list(dto)

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_order_already_exists(self, snapshot):
        dto = UpdateListDTOFactory(
            space_id="1234",
            folder_id=None,
            order=101,
            created_by="user_id",
        )

        self.interactor.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.list_permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )
        self.interactor.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": True}
        )()

        self.interactor.list_storage.check_list_order_exist_in_space.return_value = True
        self.interactor.list_storage.get_space_lists_count.return_value = 100

        with pytest.raises(InvalidOrderException) as exc:
            self.interactor.update_list(dto)

        # snapshot.assert_match(repr(exc.value), "order_already_exists.txt")
        self.interactor.list_storage.check_list_order_exist_in_space.assert_not_called()




