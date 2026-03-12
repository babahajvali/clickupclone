from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import TaskDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.tasks import BaseReorderTask


def get_task_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_task"
    )


def get_tasks_count_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_tasks_count"
    )


def get_workspace_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_workspace_id_from_task_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def shift_tasks_down_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.shift_tasks_down"
    )


def shift_tasks_up_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.shift_tasks_up"
    )


def reorder_task_storage_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.reorder_task"
    )


def reorder_task_lock_mock(mocker):
    return mocker.patch(
        "task_management.interactors.tasks.reorder_task_interactor.redis_lock",
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


def make_task_dto(order: int = 1, is_deleted: bool = False) -> TaskDTO:
    return TaskDTO(
        task_id="task_1",
        title="Task title",
        description="Task description",
        list_id="list_1",
        order=order,
        created_by="user_1",
        is_deleted=is_deleted,
    )


@pytest.mark.django_db
class TestReorderTaskAPI(BaseReorderTask):
    def _setup_common(self, mocker, role: Role = Role.MEMBER):
        get_task_mock(mocker).return_value = make_task_dto(order=1)
        get_tasks_count_mock(mocker).return_value = 3
        get_workspace_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(mocker).return_value = make_permission(role)
        reorder_task_lock_mock(mocker)

    def test_reorder_task_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        shift_tasks_down_mock(mocker)
        shift_tasks_up_mock(mocker)
        reorder_task_storage_mock(mocker).return_value = make_task_dto(order=2)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"taskId": "task_1", "order": 2}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_task_invalid_order(self, snapshot, mocker):
        self._setup_common(mocker)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"taskId": "task_1", "order": 0}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
