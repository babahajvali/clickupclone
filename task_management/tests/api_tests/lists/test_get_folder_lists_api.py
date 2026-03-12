from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ListEntityType
from task_management.interactors.dtos import ListDTO, FolderDTO
from task_management.tests.api_tests.lists import BaseGetFolderLists


def get_folder_mock(mocker):
    return mocker.patch(
        "task_management.storages.folder_storage.FolderStorage.get_folder"
    )


def get_folder_lists_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_folder_lists"
    )


def make_folder(is_deleted=False) -> FolderDTO:
    return FolderDTO(
        folder_id="folder_1",
        name="Product",
        description="Product folder",
        space_id="space_1",
        order=1,
        is_deleted=is_deleted,
        is_private=False,
        created_by="user_1",
    )


def make_list() -> ListDTO:
    return ListDTO(
        list_id="list_1",
        name="Sprint Board",
        description="List description",
        is_deleted=False,
        order=1,
        is_private=False,
        created_by="user_1",
        entity_type=ListEntityType.FOLDER,
        entity_id="folder_1",
    )


@pytest.mark.django_db
class TestGetFolderListsAPI(BaseGetFolderLists):
    def test_get_folder_lists_successfully(self, snapshot, mocker):
        get_folder = get_folder_mock(mocker)
        get_folder.return_value = make_folder()

        get_lists = get_folder_lists_mock(mocker)
        get_lists.return_value = [make_list()]

        variables = {"params": {"folderId": "folder_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_folder_lists_folder_not_found(self, snapshot, mocker):
        get_folder = get_folder_mock(mocker)
        get_folder.return_value = None

        variables = {"params": {"folderId": "folder_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
