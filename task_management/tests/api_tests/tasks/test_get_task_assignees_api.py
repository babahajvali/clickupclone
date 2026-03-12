from types import SimpleNamespace

import pytest

from task_management.interactors.dtos import TaskAssigneeDTO
from task_management.tests.api_tests.tasks import BaseGetTaskAssignees


def get_task_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_task"
    )


def get_task_assignees_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_task_assignees"
    )


@pytest.mark.django_db
class TestGetTaskAssigneesAPI(BaseGetTaskAssignees):
    def test_get_task_assignees_successfully(self, snapshot, mocker):
        get_task_mock(mocker).return_value = type("Task", (), {"is_deleted": False})()
        get_task_assignees_mock(mocker).return_value = [
            TaskAssigneeDTO(
                assign_id="assign_1",
                user_id="user_2",
                task_id="task_1",
                assigned_by="user_1",
                is_active=True,
            )
        ]

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"taskId": "task_1"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_task_assignees_not_found(self, snapshot, mocker):
        get_task_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"taskId": "task_404"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
