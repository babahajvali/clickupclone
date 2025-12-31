import pytest
from unittest.mock import create_autospec

from task_management.interactors.list_interactors.list_interactors import ListInteractor
from task_management.interactors.storage_interface.folder_storage_interface import FolderStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import ListStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import TaskStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import SpaceStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import PermissionStorageInterface
from task_management.exceptions.custom_exceptions import (
    FolderNotFoundException,
    InactiveFolderFoundException,
)


class TestGetFolderLists:

    def setup_method(self):
        self.interactor = ListInteractor(
            list_storage=create_autospec(ListStorageInterface),
            task_storage=create_autospec(TaskStorageInterface),
            folder_storage=create_autospec(FolderStorageInterface),
            space_storage=create_autospec(SpaceStorageInterface),
            permission_storage=create_autospec(PermissionStorageInterface),
        )

    def test_get_folder_lists_success(self, snapshot):
        self.interactor.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": True}
        )()
        self.interactor.list_storage.get_folder_lists.return_value = ["LIST1", "LIST2"]

        result = self.interactor.get_folder_lists("folder_1")

        snapshot.assert_match(repr(result), "get_folder_lists_success.json")

    def test_folder_not_found(self, snapshot):
        self.interactor.folder_storage.get_folder.return_value = None

        with pytest.raises(FolderNotFoundException) as exc:
            self.interactor.get_folder_lists("folder_1")

        snapshot.assert_match(repr(exc.value), "folder_not_found.txt")

    def test_folder_inactive(self, snapshot):
        self.interactor.folder_storage.get_folder.return_value = type(
            "Folder", (), {"is_active": False}
        )()

        with pytest.raises(InactiveFolderFoundException) as exc:
            self.interactor.get_folder_lists("folder_1")

        snapshot.assert_match(repr(exc.value), "folder_inactive.txt")
