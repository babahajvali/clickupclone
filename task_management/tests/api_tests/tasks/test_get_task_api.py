from types import SimpleNamespace

import pytest

from task_management.interactors.dtos import TaskDTO
from task_management.tests.api_tests.tasks import BaseGetTask


def get_task_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_task"
    )


def make_task_dto(is_deleted: bool = False) -> TaskDTO:
    return TaskDTO(
        task_id="task_1",
        title="Task title",
        description="Task description",
        list_id="list_1",
        order=1,
        created_by="user_1",
        is_deleted=is_deleted,
    )


@pytest.mark.django_db
class TestGetTaskAPI(BaseGetTask):
    def test_get_task_successfully(self, snapshot, mocker):
        get_task_mock(mocker).return_value = make_task_dto()

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"taskId": "task_1"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_task_not_found(self, snapshot, mocker):
        get_task_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"taskId": "task_404"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
