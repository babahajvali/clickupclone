from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedTaskFound,
    InactiveUser,
    ModificationNotAllowed,
    TaskNotFound,
    UserNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import TaskAssigneeDTO, \
    WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import (
    TaskStorageInterface,
    UserStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.tasks.add_task_assignee_interactor import (
    AddTaskAssigneeInteractor,
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


def make_task_assignee(assign_id: str = "assign_1") -> TaskAssigneeDTO:
    return TaskAssigneeDTO(
        assign_id=assign_id,
        task_id="task_1",
        user_id="user_2",
        assigned_by="user_1",
        is_active=True,
    )


class TestAddTaskAssigneeInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.interactor = AddTaskAssigneeInteractor(
            task_storage=self.task_storage,
            user_storage=self.user_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER):
        self.user_storage.get_user_data.return_value = type(
            "User", (), {"is_active": True}
        )()
        self.task_storage.get_task.return_value = type(
            "Task", (), {"is_deleted": False, "list_id": "list_1"}
        )()
        self.task_storage.get_user_task_assignee.return_value = None
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role)
        self.task_storage.add_task_assignee.return_value = make_task_assignee()

    def test_assign_task_assignee_success(self):
        self._setup_dependencies()

        result = self.interactor.add_task_assignee(
            task_id="task_1",
            user_id="user_2",
            assigned_by="user_1",
        )

        assert result.task_id == "task_1"
        assert result.user_id == "user_2"

    def test_assign_task_assignee_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.add_task_assignee(
                task_id="task_1",
                user_id="user_2",
                assigned_by="user_1",
            )

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_assign_task_assignee_user_not_found(self, snapshot):
        self._setup_dependencies()
        self.user_storage.get_user_data.return_value = None

        with pytest.raises(UserNotFound) as exc:
            self.interactor.add_task_assignee(
                task_id="task_1",
                user_id="user_2",
                assigned_by="user_1",
            )

        snapshot.assert_match(repr(exc.value), "user_not_found.txt")

    def test_assign_task_assignee_task_not_found(self, snapshot):
        self._setup_dependencies()
        self.task_storage.get_task.return_value = None

        with pytest.raises(TaskNotFound) as exc:
            self.interactor.add_task_assignee(
                task_id="task_1",
                user_id="user_2",
                assigned_by="user_1",
            )

        snapshot.assert_match(repr(exc.value), "task_not_found.txt")

    def test_assign_task_assignee_inactive_user(self):
        self._setup_dependencies()
        self.user_storage.get_user_data.return_value = type(
            "User", (), {"is_active": False}
        )()

        with pytest.raises(InactiveUser):
            self.interactor.add_task_assignee(
                task_id="task_1",
                user_id="user_2",
                assigned_by="user_1",
            )

    def test_assign_task_assignee_deleted_task(self, snapshot):
        self._setup_dependencies()
        self.task_storage.get_task.return_value = type(
            "Task", (), {"is_deleted": True, "list_id": "list_1"}
        )()

        with pytest.raises(DeletedTaskFound) as e:
            self.interactor.add_task_assignee(
                task_id="task_1",
                user_id="user_2",
                assigned_by="user_1",
            )

        snapshot.assert_match(repr(e.value), "deleted_task_found.txt")
