import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import Permissions, Role
from task_management.interactors.dtos import UserListPermissionDTO, \
    WorkspaceMemberDTO
from task_management.interactors.storage_interfaces.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interfaces.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.task_interactors.task_assignee_interactor import (
    TaskAssigneeInteractor
)
from task_management.interactors.storage_interfaces.task_storage_interface import (
    TaskStorageInterface
)
from task_management.interactors.storage_interfaces.task_assignee_storage_interface import (
    TaskAssigneeStorageInterface
)
from task_management.interactors.storage_interfaces.user_storage_interface import (
    UserStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowedException,
    TaskNotFoundException,
    UserNotFoundException
)
from task_management.tests.factories.interactor_factory import (
    TaskAssigneeDTOFactory, UserTasksDTOFactory
)


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )

class TestTaskAssigneeInteractor:

    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.task_assignee_storage = create_autospec(
            TaskAssigneeStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.workspace_member_storage = create_autospec(WorkspaceMemberStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)

        self.interactor = TaskAssigneeInteractor(
            task_storage=self.task_storage,
            task_assignee_storage=self.task_assignee_storage,
            user_storage=self.user_storage,
            workspace_member_storage=self.workspace_member_storage,
            list_storage=self.list_storage,
            space_storage=self.space_storage
        )

        self.interactor.user_storage = self.user_storage

    def _mock_active_task(self):
        return type(
            "Task",
            (),
            {
                "is_deleted": False,
                "list_id": "list_123"
            }
        )()

    def _mock_active_user(self):
        return type(
            "User",
            (),
            {
                "is_active": True
            }
        )()

    def test_assign_task_assignee_success(self, snapshot):
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.task_storage.get_task_by_id.return_value = self._mock_active_task()
        self.workspace_member_storage.get_workspace_member.return_value = (
            make_permission(Role.MEMBER)
        )
        self.task_assignee_storage.get_user_task_assignee.return_value = None
        task_id = "task123"
        expected = TaskAssigneeDTOFactory(task_id=task_id)
        self.task_assignee_storage.assign_task_assignee.return_value = expected

        result = self.interactor.assign_task_assignee(
            task_id=task_id,
            user_id="user123",
            assigned_by="admin123"
        )

        assert task_id == result.task_id

    def test_assign_task_assignee_permission_denied(self, snapshot):
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.task_storage.get_task_by_id.return_value = self._mock_active_task()
        self.workspace_member_storage.get_workspace_member.return_value = (
            make_permission(Role.GUEST)
        )
        self.task_assignee_storage.get_user_task_assignee.return_value = None

        with pytest.raises(ModificationNotAllowedException) as exc:
            self.interactor.assign_task_assignee(
                task_id="task123",
                user_id="user123",
                assigned_by="user456"
            )

        snapshot.assert_match(
            repr(exc.value),
            "permission_denied.txt"
        )

    def test_assign_task_assignee_user_not_found(self, snapshot):
        self.user_storage.get_user_data.return_value = None
        self.task_assignee_storage.get_user_task_assignee.return_value = None

        with pytest.raises(UserNotFoundException) as exc:
            self.interactor.assign_task_assignee(
                task_id="task123",
                user_id="user123",
                assigned_by="admin123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "user_not_found.txt"
        )

    def test_assign_task_assignee_task_not_found(self, snapshot):
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.task_storage.get_task_by_id.return_value = None
        self.task_assignee_storage.get_user_task_assignee.return_value = None

        with pytest.raises(TaskNotFoundException) as exc:
            self.interactor.assign_task_assignee(
                task_id="task123",
                user_id="user123",
                assigned_by="admin123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "task_not_found.txt"
        )

    def test_remove_task_assignee_success(self, snapshot):
        self.task_assignee_storage.get_task_assignee.return_value = type(
            "TaskAssigneeDTO", (), {"task_id": "task_1"})()

        expected = TaskAssigneeDTOFactory()
        self.task_storage.get_task_by_id.return_value = self._mock_active_task()
        self.task_assignee_storage.remove_task_assignee.return_value = expected
        self.workspace_member_storage.get_workspace_member.return_value = (
            make_permission(Role.MEMBER)
        )

        result = self.interactor.remove_task_assignee(
            assign_id="assign123",
            user_id="admin123"
        )

        snapshot.assert_match(
            repr(result),
            "remove_task_assignee_success.txt"
        )

    def test_get_task_assignee_success(self, snapshot):
        self.task_storage.get_task_by_id.return_value = self._mock_active_task()

        assignees = [TaskAssigneeDTOFactory(), TaskAssigneeDTOFactory()]
        self.task_assignee_storage.get_task_assignees.return_value = assignees

        result = self.interactor.get_task_assignees("task123")

        snapshot.assert_match(
            repr(result),
            "get_task_assignee_success.txt"
        )

    def test_get_user_assigned_tasks_success(self, snapshot):
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        tasks = [UserTasksDTOFactory(), UserTasksDTOFactory()]
        self.task_assignee_storage.get_user_assigned_tasks.return_value = tasks

        result = self.interactor.get_user_assigned_tasks("user123")

        snapshot.assert_match(
            repr(result),
            "get_user_assigned_tasks_success.txt"
        )
