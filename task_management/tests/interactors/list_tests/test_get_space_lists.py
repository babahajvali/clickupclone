import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    SpaceDeletedException,
    SpaceNotFound,
)
from task_management.interactors.dtos import ListDTO
from task_management.interactors.lists.list_interactor import ListInteractor
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    FolderStorageInterface,
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)
from django.core.cache import cache

@pytest.fixture(autouse=True)
def clear_cache_before_test():
    cache.clear()

class TestGetSpaceLists:
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

    def _setup_space_lists_dependencies(self, *, space_exists=True, space_active=True):
        self.space_storage.get_space.return_value = (
            type("Space", (), {"is_deleted": not space_active})()
            if space_exists else None
        )
        self.list_storage.get_space_lists.return_value = [
            self._get_list_dto()
        ]

    def test_get_space_lists_success(self, snapshot):
        # Arrange
        self._setup_space_lists_dependencies()

        # Act
        result = self.interactor.get_space_lists(space_id="space_1")

        # Assert
        snapshot.assert_match(repr(result), "get_space_lists_success.json")
        self.list_storage.get_space_lists.assert_called_once_with(
            space_ids=["space_1"]
        )

    def test_get_space_lists_not_found(self, snapshot):
        # Arrange
        self._setup_space_lists_dependencies(space_exists=False)

        # Act
        with pytest.raises(SpaceNotFound) as exc:
            self.interactor.get_space_lists(space_id="space_1")

        # Assert
        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_get_space_lists_inactive(self, snapshot):
        # Arrange
        self._setup_space_lists_dependencies(space_active=False)

        # Act
        with pytest.raises(SpaceDeletedException) as exc:
            self.interactor.get_space_lists(space_id="space_1")

        # Assert
        snapshot.assert_match(repr(exc.value), "space_inactive.txt")
