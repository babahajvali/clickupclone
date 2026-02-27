from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import FolderNotFound
from task_management.interactors.dtos import FolderDTO
from task_management.interactors.folders.get_folder_interactor import (
    GetFolderInteractor,
)
from task_management.interactors.storage_interfaces import FolderStorageInterface


def make_folder() -> FolderDTO:
    return FolderDTO(
        folder_id="folder_1",
        name="Folder",
        description="Desc",
        space_id="space_1",
        order=1,
        is_deleted=False,
        created_by="user_1",
        is_private=False,
    )


class TestGetFolderInteractor:
    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.interactor = GetFolderInteractor(folder_storage=self.folder_storage)

    def test_get_folder_success(self, snapshot):
        self.folder_storage.get_folder.return_value = make_folder()

        result = self.interactor.get_folder(folder_id="folder_1")

        snapshot.assert_match(repr(result), "get_folder_success.txt")

    def test_get_folder_not_found(self, snapshot):
        self.folder_storage.get_folder.return_value = None

        with pytest.raises(FolderNotFound) as exc:
            self.interactor.get_folder(folder_id="folder_1")

        snapshot.assert_match(repr(exc.value), "get_folder_not_found.txt")
