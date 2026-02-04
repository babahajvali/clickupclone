import pytest
from unittest.mock import create_autospec, patch

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import UserFolderPermissionDTO, \
    UserSpacePermissionDTO
from task_management.interactors.list_interactors.list_interactors import \
    ListInteractor
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
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
    ModificationNotAllowedException,
    SpaceNotFoundException,
    InactiveSpaceException,
)
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface
from task_management.tests.factories.interactor_factory import \
    CreateListDTOFactory


def make_folder_permission(permission_type: Permissions):
    return UserFolderPermissionDTO(
        id=1,
        folder_id="folder_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


def make_permission(permission_type: Permissions):
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

    @patch(
        "task_management.interactors.list_interactors.list_interactors.CreateTemplateInteractor.create_template"
    )
    def test_create_list_success(self, mock_create_template, snapshot):
        mock_create_template.return_value = None

        dto = CreateListDTOFactory(folder_id="folder_123",
                                   space_id="space_123")

        self.folder_permission_storage.get_user_permission_for_folder.return_value = (
            make_folder_permission(Permissions.FULL_EDIT.value)
        )

        self.list_storage.create_list.return_value = type("List", (), {
            "list_id": "list_id",
            "created_by": "user_id",
            "space_id": "space_123", })()

        result = self.interactor.create_list(dto)

        # snapshot.assert_match(
        #     repr(result),
        #     "test_create_list_success.txt"
        # )
        self.list_storage.create_list.assert_called_once()

    def test_permission_denied(self, snapshot):
        dto = CreateListDTOFactory(folder_id=None)

        self.space_permission_storage.get_user_permission_for_space.return_value = make_permission(
            Permissions.VIEW.value
        )

        with pytest.raises(ModificationNotAllowedException) as exc:
            self.interactor.create_list(dto)

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    @patch(
        "task_management.interactors.list_interactors.list_interactors.CreateTemplateInteractor.create_template"
    )
    def test_space_not_found(self, mock_create_template, snapshot):
        mock_create_template.return_value = None

        dto = CreateListDTOFactory(folder_id=None)
        dto.space_id = "space_123"  # ✅ REQUIRED

        self.space_permission_storage.get_user_permission_for_space.return_value = (
            make_permission(Permissions.FULL_EDIT.value)
        )
        self.space_storage.get_space.return_value = None

        with pytest.raises(SpaceNotFoundException):
            self.interactor.create_list(dto)

    @patch(
        "task_management.interactors.list_interactors.list_interactors.CreateTemplateInteractor.create_template"
    )
    def test_space_inactive(self, mock_create_template, snapshot):
        mock_create_template.return_value = None

        dto = CreateListDTOFactory(folder_id=None)
        dto.space_id = "space_123"

        self.space_permission_storage.get_user_permission_for_space.return_value = (
            make_permission(Permissions.FULL_EDIT.value)
        )
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": False}
        )()

        with pytest.raises(InactiveSpaceException):
            self.interactor.create_list(dto)
