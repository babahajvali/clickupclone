from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import SpaceNotFound
from task_management.interactors.dtos import FolderDTO
from task_management.interactors.folders.get_space_folders_interactor import (
    GetSpaceFoldersInteractor,
)
from task_management.interactors.storage_interfaces import (
    FolderStorageInterface,
    SpaceStorageInterface,
)


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


class TestGetSpaceFoldersInteractor:
    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)

        self.interactor = GetSpaceFoldersInteractor(
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
        )

    def test_get_space_folders_success(self, snapshot):
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_deleted": False}
        )()
        self.folder_storage.get_space_folders.return_value = [make_folder()]

        result = self.interactor.get_space_folders(space_id="space_1")

        snapshot.assert_match(repr(result), "get_space_folders_success.txt")

    def test_get_space_folders_space_not_found(self, snapshot):
        self.space_storage.get_space.return_value = None

        with pytest.raises(SpaceNotFound) as exc:
            self.interactor.get_space_folders(space_id="space_1")

        snapshot.assert_match(
            repr(exc.value), "get_space_folders_space_not_found.txt"
        )
