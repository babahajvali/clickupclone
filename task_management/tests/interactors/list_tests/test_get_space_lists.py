from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedSpaceFound,
    SpaceNotFound,
)
from task_management.exceptions.enums import ListEntityType
from task_management.interactors.dtos import ListDTO
from task_management.interactors.lists.get_space_lists_interactor import (
    GetSpaceListsInteractor,
)
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    SpaceStorageInterface,
)


class TestGetSpaceLists:
    @staticmethod
    def _get_list_dto():
        return ListDTO(
            list_id="list_1",
            name="List name",
            description="List description",
            is_deleted=False,
            order=1,
            is_private=False,
            created_by="user_id",
            entity_type=ListEntityType.SPACE,
            entity_id="space_1",
        )

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)

        self.interactor = GetSpaceListsInteractor(
            list_storage=self.list_storage,
            space_storage=self.space_storage,
        )

    def _setup_space_lists_dependencies(self, *, space_exists=True,
                                        space_active=True):
        self.space_storage.get_space.return_value = (
            type("Space", (), {"is_deleted": not space_active})()
            if space_exists
            else None
        )
        self.list_storage.get_space_lists.return_value = [self._get_list_dto()]

    def test_get_space_lists_success(self, snapshot):
        # Arrange
        self._setup_space_lists_dependencies()

        # Act
        result = self.interactor.get_space_lists(space_id="space_1")

        # Assert
        snapshot.assert_match(repr(result), "get_space_lists_success.json")
        self.list_storage.get_space_lists.assert_called_once_with(
            space_ids=["space_1"])

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
        with pytest.raises(DeletedSpaceFound) as exc:
            self.interactor.get_space_lists(space_id="space_1")

        # Assert
        snapshot.assert_match(repr(exc.value), "space_inactive.txt")
