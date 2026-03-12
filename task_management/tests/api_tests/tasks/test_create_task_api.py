from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import TaskDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.tasks import BaseCreateTask


def get_list_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_list"
    )


def get_workspace_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_workspace_id_by_list_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def get_last_task_order_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_last_task_order_in_list"
    )


def create_task_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.create_task"
    )


def get_template_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.list_storage.ListStorage.get_template_id_by_list_id"
    )


def get_fields_for_template_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.get_fields_for_template"
    )


def create_bulk_field_values_mock(mocker):
    return mocker.patch(
        "task_management.storages.field_storage.FieldStorage.create_bulk_field_values"
    )


def create_task_lock_mock(mocker):
    return mocker.patch(
        "task_management.interactors.tasks.create_task_interactor.redis_lock",
        return_value=nullcontext(),
    )


def make_permission(role: Role = Role.MEMBER) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        role=role,
        user_id="user_1",
        is_active=True,
        added_by="admin_1",
    )


def make_task_dto(order: int = 2) -> TaskDTO:
    return TaskDTO(
        task_id="task_1",
        title="Task title",
        description="Task description",
        list_id="list_1",
        order=order,
        created_by="user_1",
        is_deleted=False,
    )


@pytest.mark.django_db
class TestCreateTaskAPI(BaseCreateTask):
    def _setup_common(self, mocker, role: Role = Role.MEMBER):
        get_list_mock(mocker).return_value = type(
            "List", (), {"is_deleted": False}
        )()
        get_workspace_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(mocker).return_value = make_permission(role)
        get_last_task_order_mock(mocker).return_value = 1
        get_template_id_mock(mocker).return_value = "template_1"
        get_fields_for_template_mock(mocker).return_value = []
        create_bulk_field_values_mock(mocker).return_value = []
        create_task_lock_mock(mocker)

    def test_create_task_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        create_task_mock(mocker).return_value = make_task_dto(order=2)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {
                "title": "Task title",
                "description": "Task description",
                "listId": "list_1",
            }},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_task_list_not_found(self, snapshot, mocker):
        get_list_mock(mocker).return_value = None
        create_task_lock_mock(mocker)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {
                "title": "Task title",
                "description": "Task description",
                "listId": "list_404",
            }},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_task_empty_title(self, snapshot, mocker):
        create_task_lock_mock(mocker)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {
                "title": "   ",
                "description": "Task description",
                "listId": "list_1",
            }},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
