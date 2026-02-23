import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    FolderNotFound,
    InactiveFolder,
)
from task_management.interactors.dtos import ListDTO
from task_management.interactors.lists.list_interactor import ListInteractor
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    FolderStorageInterface,
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)


class TestGetFolderLists:
    @staticmethod
    def _get_list_dto():
        return ListDTO(
            list_id="list_1",
            name="List name",
            description="List description",
            space_id="space_1",
            is_active=True,
            order=1,
            is_private=False,
            created_by="user_id",
            folder_id="folder_1",
        )

    def _get_interactor(self, *, folder_exists=True, folder_active=True):
        list_storage = create_autospec(ListStorageInterface)
        folder_storage = create_autospec(FolderStorageInterface)
        space_storage = create_autospec(SpaceStorageInterface)
        workspace_storage = create_autospec(WorkspaceStorageInterface)

        folder_storage.get_folder.return_value = (
            type("Folder", (), {"is_active": folder_active})()
            if folder_exists else None
        )
        list_storage.get_active_folder_lists.return_value = [
            self._get_list_dto()
        ]

        return ListInteractor(
            list_storage=list_storage,
            folder_storage=folder_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

    def test_get_folder_lists_success(self, snapshot):
        interactor = self._get_interactor()

        result = interactor.get_active_folder_lists(folder_id="folder_1")

        snapshot.assert_match(
            repr(result),
            "test_get_folder_lists_success.txt",
        )

    def test_get_folder_lists_not_found(self, snapshot):
        interactor = self._get_interactor(folder_exists=False)

        with pytest.raises(FolderNotFound) as exc:
            interactor.get_active_folder_lists(folder_id="folder_1")

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "test_get_folder_lists_not_found.txt",
        )

    def test_get_folder_lists_inactive(self, snapshot):
        interactor = self._get_interactor(folder_active=False)

        with pytest.raises(InactiveFolder) as exc:
            interactor.get_active_folder_lists(folder_id="folder_1")

        snapshot.assert_match(
            repr(exc.value.folder_id),
            "test_get_folder_lists_inactive.txt",
        )
