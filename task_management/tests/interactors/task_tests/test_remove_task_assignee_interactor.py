from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    InActiveTaskAssigneeFound,
    ModificationNotAllowed,
    TaskAssigneeNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import TaskAssigneeDTO, WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import (
    TaskStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.tasks.remove_task_assignee_interactor import (
    RemoveTaskAssigneeInteractor,
)


def make_task_assignee(is_active: bool = True) -> TaskAssigneeDTO:
    return TaskAssigneeDTO(
        assign_id="assign_1",
        task_id="task_1",
        user_id="user_2",
        assigned_by="user_1",
        is_active=is_active,
    )


def make_permission(role: Role = Role.MEMBER) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        user_id="user_1",
        role=role,
        is_active=True,
        added_by="admin_1",
    )


class TestRemoveTaskAssigneeInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.interactor = RemoveTaskAssigneeInteractor(
            task_storage=self.task_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER):
        self.task_storage.get_task_assignee.return_value = make_task_assignee(
            is_active=True
        )
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(role)
        self.task_storage.remove_task_assignee.return_value = make_task_assignee(
            is_active=False
        )

    def test_remove_task_assignee_success(self, snapshot):
        self._setup_dependencies()

        result = self.interactor.remove_task_assignee(
            assign_id="assign_1",
            user_id="user_1",
        )

        snapshot.assert_match(repr(result), "remove_task_assignee_success.txt")

    def test_remove_task_assignee_not_found(self):
        self.task_storage.get_task_assignee.return_value = None

        with pytest.raises(TaskAssigneeNotFound):
            self.interactor.remove_task_assignee(
                assign_id="missing_assign",
                user_id="user_1",
            )

    def test_remove_task_assignee_inactive(self):
        self.task_storage.get_task_assignee.return_value = make_task_assignee(
            is_active=False
        )

        with pytest.raises(InActiveTaskAssigneeFound):
            self.interactor.remove_task_assignee(
                assign_id="assign_1",
                user_id="user_1",
            )

    def test_remove_task_assignee_permission_denied(self):
        self._setup_dependencies(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed):
            self.interactor.remove_task_assignee(
                assign_id="assign_1",
                user_id="user_1",
            )
