import pytest

from task_management.interactors.dtos import FolderDTO, SpaceDTO
from task_management.tests.api_tests.folders import BaseGetSpaceFolders


def get_space_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_space"
    )


def get_space_folders_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.get_space_folders"
    )


def make_space(is_deleted=False) -> SpaceDTO:
    return SpaceDTO(
        space_id="space_1",
        name="Engineering",
        description="Engineering space",
        workspace_id="workspace_1",
        order=1,
        is_deleted=is_deleted,
        is_private=False,
        created_by="user_1",
    )


def make_folder(folder_id="folder_1", order=1) -> FolderDTO:
    return FolderDTO(
        folder_id=folder_id,
        name="Product",
        description="Product folder",
        space_id="space_1",
        order=order,
        is_deleted=False,
        is_private=False,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestGetSpaceFoldersAPI(BaseGetSpaceFolders):
    def test_get_space_folders_successfully(self, snapshot, mocker):
        get_space = get_space_mock(mocker)
        get_space.return_value = make_space()

        get_folders = get_space_folders_mock(mocker)
        get_folders.return_value = [
            make_folder(folder_id="folder_1", order=1),
            make_folder(folder_id="folder_2", order=2),
        ]

        variables = {"params": {"spaceId": "space_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_get_space_folders_space_not_found(self, snapshot, mocker):
        get_space = get_space_mock(mocker)
        get_space.return_value = None

        variables = {"params": {"spaceId": "space_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )
