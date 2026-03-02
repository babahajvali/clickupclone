from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    InActiveTaskAssigneeFound,
    ModificationNotAllowed,
    TaskAssigneeNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces import (
    TaskStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.tasks.remove_task_assignee_interactor import (
    RemoveTaskAssigneeInteractor,
)
from task_management.tests.interactors.task_tests.test_helpers import (
    make_permission,
    make_task_assignee,
)


class TestRemoveTaskAssigneeInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.interactor = RemoveTaskAssigneeInteractor(
            task_storage=self.task_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_remove_task_assignee_success(self, snapshot):
        self.task_storage.get_task_assignee.return_value = make_task_assignee(
            assign_id="assign_1",
            task_id="task_1",
            user_id="user_2",
            assigned_by="user_1",
            is_active=True,
        )
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission()
        self.task_storage.remove_task_assignee.return_value = make_task_assignee(
            assign_id="assign_1",
            task_id="task_1",
            user_id="user_2",
            assigned_by="user_1",
            is_active=False,
        )

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
            assign_id="assign_1",
            is_active=False,
        )

        with pytest.raises(InActiveTaskAssigneeFound):
            self.interactor.remove_task_assignee(
                assign_id="assign_1",
                user_id="user_1",
            )

    def test_remove_task_assignee_permission_denied(self):
        self.task_storage.get_task_assignee.return_value = make_task_assignee(
            assign_id="assign_1",
            task_id="task_1",
            is_active=True,
        )
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role=Role.GUEST
        )

        with pytest.raises(ModificationNotAllowed):
            self.interactor.remove_task_assignee(
                assign_id="assign_1",
                user_id="user_1",
            )
