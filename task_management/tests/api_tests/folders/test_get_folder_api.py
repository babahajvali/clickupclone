import pytest

from task_management.interactors.dtos import FolderDTO
from task_management.tests.api_tests.folders import BaseGetFolder


def get_folder_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.get_folder"
    )


def make_folder() -> FolderDTO:
    return FolderDTO(
        folder_id="folder_1",
        name="Product",
        description="Product folder",
        space_id="space_1",
        order=1,
        is_deleted=False,
        is_private=False,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestGetFolderAPI(BaseGetFolder):
    def test_get_folder_successfully(self, snapshot, mocker):
        get_folder = get_folder_mock(mocker)
        get_folder.return_value = make_folder()

        variables = {"params": {"folderId": "folder_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_get_folder_not_found(self, snapshot, mocker):
        get_folder = get_folder_mock(mocker)
        get_folder.return_value = None

        variables = {"params": {"folderId": "folder_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )
