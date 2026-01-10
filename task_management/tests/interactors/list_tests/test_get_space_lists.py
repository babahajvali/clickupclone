import pytest
from unittest.mock import create_autospec

from task_management.interactors.list_interactors.list_interactors import ListInteractor
from task_management.interactors.storage_interface.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import SpaceStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import ListStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import TaskStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import FolderStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import SpacePermissionStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import ListPermissionStorageInterface
from task_management.interactors.storage_interface.folder_permission_storage_interface import FolderPermissionStorageInterface
from task_management.exceptions.custom_exceptions import (
    SpaceNotFoundException,
    InactiveSpaceException,
)
from task_management.interactors.storage_interface.template_storage_interface import \
    TemplateStorageInterface


class TestGetSpaceLists:

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

    def test_get_space_lists_success(self, snapshot):
        self.interactor.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": True}
        )()
        self.interactor.list_storage.get_space_lists.return_value = ["LIST1"]

        result = self.interactor.get_space_lists("space_1")

        snapshot.assert_match(repr(result), "get_space_lists_success.json")

    def test_space_not_found(self, snapshot):
        self.interactor.space_storage.get_space.return_value = None

        with pytest.raises(SpaceNotFoundException) as exc:
            self.interactor.get_space_lists("space_1")

        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_space_inactive(self, snapshot):
        self.interactor.space_storage.get_space.return_value = type(
            "Space", (), {"is_active": False}
        )()

        with pytest.raises(InactiveSpaceException) as exc:
            self.interactor.get_space_lists("space_1")

        snapshot.assert_match(repr(exc.value), "space_inactive.txt")
