from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ListEntityType
from task_management.interactors.dtos import ListDTO, SpaceDTO
from task_management.tests.api_tests.lists import BaseGetSpaceLists


def get_space_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_space"
    )


def get_space_lists_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_space_lists"
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


def make_list() -> ListDTO:
    return ListDTO(
        list_id="list_1",
        name="Sprint Board",
        description="List description",
        is_deleted=False,
        order=1,
        is_private=False,
        created_by="user_1",
        entity_type=ListEntityType.SPACE,
        entity_id="space_1",
    )


@pytest.mark.django_db
class TestGetSpaceListsAPI(BaseGetSpaceLists):
    def test_get_space_lists_successfully(self, snapshot, mocker):
        get_space = get_space_mock(mocker)
        get_space.return_value = make_space()

        get_lists = get_space_lists_mock(mocker)
        get_lists.return_value = [make_list()]

        variables = {"params": {"spaceId": "space_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_space_lists_space_not_found(self, snapshot, mocker):
        get_space = get_space_mock(mocker)
        get_space.return_value = None

        variables = {"params": {"spaceId": "space_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
