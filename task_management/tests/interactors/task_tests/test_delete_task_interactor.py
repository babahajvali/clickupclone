from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    TaskNotFound,
    UserNotWorkspaceMember,
)
from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces import (
    TaskStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.tasks.delete_task_interactor import (
    DeleteTaskInteractor,
)
from task_management.tests.interactors.task_tests.test_helpers import (
    make_permission,
    make_task,
)


class TestDeleteTaskInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.interactor = DeleteTaskInteractor(
            task_storage=self.task_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_delete_task_success(self, snapshot):
        self.task_storage.get_task.return_value = make_task(task_id="task_1")
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission()
        self.task_storage.delete_task.return_value = make_task(
            task_id="task_1",
            is_deleted=True,
        )

        result = self.interactor.delete_task(task_id="task_1", user_id="user_1")

        snapshot.assert_match(repr(result), "test_delete_task_success.txt")

    def test_delete_task_not_found(self, snapshot):
        self.task_storage.get_task.return_value = None

        with pytest.raises(TaskNotFound) as exc:
            self.interactor.delete_task(task_id="missing_task", user_id="user_1")

        snapshot.assert_match(repr(exc.value), "test_delete_task_not_found.txt")

    def test_delete_task_permission_denied(self, snapshot):
        self.task_storage.get_task.return_value = make_task(task_id="task_1")
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role=Role.GUEST
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.delete_task(task_id="task_1", user_id="user_1")

        snapshot.assert_match(
            repr(exc.value),
            "test_delete_task_permission_denied.txt",
        )

    def test_delete_task_user_not_workspace_member(self):
        self.task_storage.get_task.return_value = make_task(task_id="task_1")
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = None

        with pytest.raises(UserNotWorkspaceMember):
            self.interactor.delete_task(task_id="task_1", user_id="user_1")
