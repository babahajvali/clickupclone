from unittest.mock import create_autospec

import pytest
from django.core.cache import cache

from task_management.exceptions.custom_exceptions import (
    DeletedFolderException,
    FolderNotFound,
)
from task_management.interactors.dtos import ListDTO
from task_management.interactors.lists.get_folder_lists_interactor import (
    GetFolderListsInteractor,
)
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    FolderStorageInterface,
)


@pytest.fixture(autouse=True)
def clear_cache_before_test():
    cache.clear()


class TestGetFolderLists:
    @staticmethod
    def _get_list_dto():
        return ListDTO(
            list_id="list_1",
            name="List name",
            description="List description",
            space_id="space_1",
            is_deleted=False,
            order=1,
            is_private=False,
            created_by="user_id",
            folder_id="folder_1",
        )

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)

        self.interactor = GetFolderListsInteractor(
            list_storage=self.list_storage, folder_storage=self.folder_storage
        )

    def _setup_folder_lists_dependencies(
            self, *, folder_exists=True, folder_active=True
    ):
        self.folder_storage.get_folder.return_value = (
            type("Folder", (), {"is_deleted": not folder_active})()
            if folder_exists
            else None
        )
        self.list_storage.get_folder_lists.return_value = [
            self._get_list_dto()]

    def test_get_folder_lists_success(self, snapshot):
        # Arrange
        self._setup_folder_lists_dependencies()

        # Act
        result = self.interactor.get_folder_lists(folder_id="folder_1")

        # Assert
        snapshot.assert_match(repr(result), "get_folder_lists_success.json")
        self.list_storage.get_folder_lists.assert_called_once_with(
            folder_ids=["folder_1"]
        )

    def test_get_folder_lists_not_found(self, snapshot):
        # Arrange
        self.folder_storage.get_folder.return_value = None

        # Act
        with pytest.raises(FolderNotFound) as exc:
            self.interactor.get_folder_lists(folder_id="folder_1")

        # Assert
        snapshot.assert_match(repr(exc.value), "folder_not_found.txt")

    def test_get_folder_lists_inactive(self, snapshot):
        # Arrange
        self._setup_folder_lists_dependencies(folder_active=False)

        # Act
        with pytest.raises(DeletedFolderException) as exc:
            self.interactor.get_folder_lists(folder_id="folder_1")

        # Assert
        snapshot.assert_match(repr(exc.value), "folder_inactive.txt")
