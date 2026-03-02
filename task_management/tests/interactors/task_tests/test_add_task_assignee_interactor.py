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
from task_management.interactors.storage_interfaces import (
    TaskStorageInterface,
    UserStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.tasks.add_task_assignee_interactor import (
    AddTaskAssigneeInteractor,
)
from task_management.tests.interactors.task_tests.test_helpers import (
    make_permission,
    make_task_assignee,
    make_task_data,
    make_user,
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

    def test_assign_task_assignee_success(self):
        self.user_storage.get_user_data.return_value = make_user()
        self.task_storage.get_task.return_value = make_task_data()
        self.task_storage.get_user_task_assignee.return_value = None
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission()
        self.task_storage.add_task_assignee.return_value = make_task_assignee(
            task_id="task_1",
            user_id="user_2",
            assigned_by="user_1",
        )

        result = self.interactor.add_task_assignee(
            task_id="task_1",
            user_id="user_2",
            assigned_by="user_1",
        )

        assert result.task_id == "task_1"
        assert result.user_id == "user_2"

    def test_assign_task_assignee_permission_denied(self, snapshot):
        self.user_storage.get_user_data.return_value = make_user()
        self.task_storage.get_task.return_value = make_task_data()
        self.task_storage.get_user_task_assignee.return_value = None
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role=Role.GUEST
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.add_task_assignee(
                task_id="task_1",
                user_id="user_2",
                assigned_by="user_1",
            )

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_assign_task_assignee_user_not_found(self, snapshot):
        self.task_storage.get_user_task_assignee.return_value = None
        self.task_storage.get_task.return_value = make_task_data()
        self.user_storage.get_user_data.return_value = None

        with pytest.raises(UserNotFound) as exc:
            self.interactor.add_task_assignee(
                task_id="task_1",
                user_id="user_2",
                assigned_by="user_1",
            )

        snapshot.assert_match(repr(exc.value), "user_not_found.txt")

    def test_assign_task_assignee_task_not_found(self, snapshot):
        self.task_storage.get_user_task_assignee.return_value = None
        self.task_storage.get_task.return_value = None

        with pytest.raises(TaskNotFound) as exc:
            self.interactor.add_task_assignee(
                task_id="task_1",
                user_id="user_2",
                assigned_by="user_1",
            )

        snapshot.assert_match(repr(exc.value), "task_not_found.txt")

    def test_assign_task_assignee_inactive_user(self):
        self.task_storage.get_user_task_assignee.return_value = None
        self.task_storage.get_task.return_value = make_task_data()
        self.user_storage.get_user_data.return_value = make_user(is_active=False)

        with pytest.raises(InactiveUser):
            self.interactor.add_task_assignee(
                task_id="task_1",
                user_id="user_2",
                assigned_by="user_1",
            )

    def test_assign_task_assignee_deleted_task(self):
        self.task_storage.get_user_task_assignee.return_value = None
        self.task_storage.get_task.return_value = make_task_data(is_deleted=True)

        with pytest.raises(DeletedTaskFound):
            self.interactor.add_task_assignee(
                task_id="task_1",
                user_id="user_2",
                assigned_by="user_1",
            )

    def test_assign_task_assignee_existing_assignee_reassigns(self):
        existing_assignee = make_task_assignee(assign_id="assign_existing")
        self.task_storage.get_user_task_assignee.return_value = existing_assignee
        self.task_storage.reassign_task_assignee.return_value = make_task_assignee(
            assign_id="assign_existing",
            is_active=True,
        )

        result = self.interactor.add_task_assignee(
            task_id="task_1",
            user_id="user_2",
            assigned_by="user_1",
        )

        self.task_storage.reassign_task_assignee.assert_called_once_with(
            assign_id="assign_existing"
        )
        self.task_storage.get_task.assert_not_called()
        self.user_storage.get_user_data.assert_not_called()
        assert result.assign_id == "assign_existing"
