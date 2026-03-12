from types import SimpleNamespace

import pytest

from task_management.interactors.dtos import TaskDTO, TaskAssigneeDTO, \
    TaskFieldValuesDTO, FieldValueDTO
from task_management.tests.api_tests.tasks import BaseGetListTasks


def get_list_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_list"
    )


def get_tasks_for_list_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_tasks_for_list"
    )


def get_assignees_for_list_tasks_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_assignees_for_list_tasks"
    )


def get_field_values_by_task_ids_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_field_values_by_task_ids"
    )


def make_task_dto(task_id: str) -> TaskDTO:
    return TaskDTO(
        task_id=task_id,
        title="Task title",
        description="Task description",
        list_id="list_1",
        order=1,
        created_by="user_1",
        is_deleted=False,
    )


@pytest.mark.django_db
class TestGetListTasksAPI(BaseGetListTasks):
    def test_get_list_tasks_successfully(self, snapshot, mocker):
        get_list_mock(mocker).return_value = type("List", (), {"is_deleted": False})()
        get_tasks_for_list_mock(mocker).return_value = [make_task_dto("task_1")]
        get_assignees_for_list_tasks_mock(mocker).return_value = [
            TaskAssigneeDTO(
                assign_id="assign_1",
                user_id="user_2",
                task_id="task_1",
                assigned_by="user_1",
                is_active=True,
            )
        ]
        get_field_values_by_task_ids_mock(mocker).return_value = [
            TaskFieldValuesDTO(
                task_id="task_1",
                values=[FieldValueDTO(field_id="field_1", value="high")],
            )
        ]

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listId": "list_1"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_list_tasks_not_found(self, snapshot, mocker):
        get_list_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"listId": "list_404"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
