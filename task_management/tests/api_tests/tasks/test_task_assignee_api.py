from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import TaskAssigneeDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.tasks import BaseTaskAssignee


def get_task_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_task"
    )


def get_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.get_user"
    )


def get_workspace_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_workspace_id_from_task_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def get_user_task_assignee_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_user_task_assignee"
    )


def add_task_assignee_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.add_task_assignee"
    )


def get_task_assignee_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_task_assignee"
    )


def remove_task_assignee_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.remove_task_assignee"
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


def make_task_assignee_dto(is_active: bool = True) -> TaskAssigneeDTO:
    return TaskAssigneeDTO(
        assign_id="assign_1",
        task_id="task_1",
        user_id="user_2",
        assigned_by="user_1",
        is_active=is_active,
    )


@pytest.mark.django_db
class TestTaskAssigneeAPI(BaseTaskAssignee):
    def _setup_create_common(self, mocker, role: Role = Role.MEMBER):
        get_task_mock(mocker).return_value = type(
            "Task", (), {"is_deleted": False}
        )()
        get_user_mock(mocker).return_value = type(
            "User", (), {"is_active": True}
        )()
        get_workspace_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(mocker).return_value = make_permission(role)
        get_user_task_assignee_mock(mocker).return_value = None

    def test_add_task_assignee_successfully(self, snapshot, mocker):
        self._setup_create_common(mocker)
        add_task_assignee_mock(mocker).return_value = make_task_assignee_dto()

        self.execute_schema(
            query=self.CREATE_QUERY,
            variables={"params": {"taskId": "task_1", "userId": "user_2"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_add_task_assignee_task_not_found(self, snapshot, mocker):
        get_task_mock(mocker).return_value = None
        get_user_mock(mocker).return_value = type("User", (), {"is_active": True})()

        self.execute_schema(
            query=self.CREATE_QUERY,
            variables={"params": {"taskId": "task_404", "userId": "user_2"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_remove_task_assignee_successfully(self, snapshot, mocker):
        get_task_assignee_mock(mocker).return_value = make_task_assignee_dto()
        get_workspace_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(mocker).return_value = make_permission()
        remove_task_assignee_mock(mocker).return_value = make_task_assignee_dto(
            is_active=False,
        )

        self.execute_schema(
            query=self.REMOVE_QUERY,
            variables={"params": {"assignId": "assign_1"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
