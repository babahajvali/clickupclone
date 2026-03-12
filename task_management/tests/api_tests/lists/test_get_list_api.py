from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import ListEntityType
from task_management.interactors.dtos import ListDTO
from task_management.tests.api_tests.lists import BaseGetList


def get_list_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_list"
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
class TestGetListAPI(BaseGetList):
    def test_get_list_successfully(self, snapshot, mocker):
        get_list = get_list_mock(mocker)
        get_list.return_value = make_list()

        variables = {"params": {"listId": "list_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_list_not_found(self, snapshot, mocker):
        get_list = get_list_mock(mocker)
        get_list.return_value = None

        variables = {"params": {"listId": "list_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
