from types import SimpleNamespace

import pytest

from task_management.interactors.dtos import TaskDTO
from task_management.tests.api_tests.tasks import BaseTaskFilter


def get_list_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_list"
    )


def task_filter_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.task_filter_data"
    )


def make_task_dto() -> TaskDTO:
    return TaskDTO(
        task_id="task_1",
        title="Task title",
        description="Task description",
        list_id="list_1",
        order=1,
        created_by="user_1",
        is_deleted=False,
    )


@pytest.mark.django_db
class TestTaskFilterAPI(BaseTaskFilter):
    def test_task_filter_successfully(self, snapshot, mocker):
        get_list_mock(mocker).return_value = type("List", (), {"is_deleted": False})()
        task_filter_mock(mocker).return_value = [make_task_dto()]

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {
                "listId": "list_1",
                "fieldFilters": "{\"priority\": [\"high\"]}",
                "assignees": ["user_1"],
                "offset": 1,
                "limit": 10,
            }},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_task_filter_invalid_offset(self, snapshot, mocker):
        get_list_mock(mocker).return_value = type("List", (), {"is_deleted": False})()

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {
                "listId": "list_1",
                "fieldFilters": "{\"priority\": [\"high\"]}",
                "assignees": ["user_1"],
                "offset": 0,
                "limit": 10,
            }},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
