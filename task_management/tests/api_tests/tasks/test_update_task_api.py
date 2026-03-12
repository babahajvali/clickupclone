from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import TaskDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.tasks import BaseUpdateTask


def get_task_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_task"
    )


def get_workspace_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_workspace_id_from_task_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def update_task_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.update_task"
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


def make_task_dto(is_deleted: bool = False) -> TaskDTO:
    return TaskDTO(
        task_id="task_1",
        title="Updated title",
        description="Updated description",
        list_id="list_1",
        order=1,
        created_by="user_1",
        is_deleted=is_deleted,
    )


@pytest.mark.django_db
class TestUpdateTaskAPI(BaseUpdateTask):
    def _setup_common(self, mocker, role: Role = Role.MEMBER):
        get_task_mock(mocker).return_value = make_task_dto()
        get_workspace_id_mock(mocker).return_value = "workspace_1"
        get_workspace_member_mock(mocker).return_value = make_permission(role)

    def test_update_task_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        update_task_mock(mocker).return_value = make_task_dto()

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {
                "taskId": "task_1",
                "title": "Updated title",
                "description": "Updated description",
            }},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_task_not_found(self, snapshot, mocker):
        get_task_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {
                "taskId": "task_404",
                "title": "Updated title",
            }},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_task_deleted(self, snapshot, mocker):
        self._setup_common(mocker)
        get_task_mock(mocker).return_value = make_task_dto(is_deleted=True)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {
                "taskId": "task_1",
                "title": "Updated title",
            }},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
