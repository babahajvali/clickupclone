import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    DeletedListFound,
    ListNotFound,
)
from task_management.interactors.dtos import ListDTO
from task_management.interactors.lists.list_interactor import ListInteractor
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    FolderStorageInterface,
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)


class TestGetActiveList:
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
            folder_id=None,
        )

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = ListInteractor(
            list_storage=self.list_storage,
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_get_list_dependencies(self, *, list_data=None):
        if list_data is None:
            list_data = self._get_list_dto()

        self.list_storage.get_list.return_value = list_data

    def test_get_active_list_success(self, snapshot):
        # Arrange
        self._setup_get_list_dependencies()

        # Act
        result = self.interactor.get_list(list_id="list_1")

        # Assert
        snapshot.assert_match(repr(result), "test_get_active_list_success.txt")
        self.list_storage.get_list.assert_called_with(list_id="list_1")

    def test_get_active_list_not_found(self, snapshot):
        # Arrange
        self._setup_get_list_dependencies(list_data=None)
        self.list_storage.get_list.return_value = None

        # Act
        with pytest.raises(ListNotFound) as exc:
            self.interactor.get_list(list_id="list_1")

        # Assert
        snapshot.assert_match(repr(exc.value), "test_get_active_list_not_found.txt")


