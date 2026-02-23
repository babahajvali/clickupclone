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

    def _get_interactor(self, *, space_exists=True, space_active=True):
        list_storage = create_autospec(ListStorageInterface)
        folder_storage = create_autospec(FolderStorageInterface)
        space_storage = create_autospec(SpaceStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        space_storage.get_space.return_value = (
            type("Space", (), {"is_deleted": not space_active})()
            if space_exists else None
        )
        list_storage.get_space_lists.return_value = [
            self._get_list_dto()
        ]

        return ListInteractor(
            list_storage=list_storage,
            folder_storage=folder_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

    def test_get_space_lists_success(self):
        interactor = self._get_interactor()

        result = interactor.get_space_lists(space_id="space_1")

        assert len(result) == 1
        assert result[0].space_id == "space_1"
        interactor.list_storage.get_space_lists.assert_called_once_with(
            space_ids=["space_1"]
        )

    def test_get_space_lists_not_found(self):
        interactor = self._get_interactor(space_exists=False)

        with pytest.raises(SpaceNotFound) as exc:
            interactor.get_space_lists(space_id="space_1")

        assert exc.value.space_id == "space_1"

    def test_get_space_lists_inactive(self):
        interactor = self._get_interactor(space_active=False)

        with pytest.raises(SpaceDeletedException) as exc:
            interactor.get_space_lists(space_id="space_1")

        assert exc.value.space_id == "space_1"
