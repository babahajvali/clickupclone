from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedTaskFound,
    TaskNotFound,
)
from task_management.interactors.dtos import TaskAssigneeDTO
from task_management.interactors.storage_interfaces import TaskStorageInterface
from task_management.interactors.tasks.get_task_assignees import (
    GetTaskAssigneesInteractor,
)


def make_task(is_deleted: bool = False):
    return type("Task", (), {"is_deleted": is_deleted, "list_id": "list_1"})()


def make_task_assignee(assign_id: str, user_id: str) -> TaskAssigneeDTO:
    return TaskAssigneeDTO(
        assign_id=assign_id,
        user_id=user_id,
        task_id="task_1",
        assigned_by="user_1",
        is_active=True,
    )


class TestGetTaskAssigneesInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.interactor = GetTaskAssigneesInteractor(
            task_storage=self.task_storage)

    def _setup_dependencies(self):
        self.task_storage.get_task.return_value = make_task()
        self.task_storage.get_task_assignees.return_value = [
            make_task_assignee(assign_id="assign_1", user_id="user_2"),
            make_task_assignee(assign_id="assign_2", user_id="user_3"),
        ]

    def test_get_task_assignee_success(self, snapshot):
        self._setup_dependencies()

        result = self.interactor.get_task_assignees(task_id="task_1")

        snapshot.assert_match(repr(result), "get_task_assignee_success.txt")

    def test_get_task_assignee_task_not_found(self):
        self.task_storage.get_task.return_value = None

        with pytest.raises(TaskNotFound):
            self.interactor.get_task_assignees(task_id="task_1")

    def test_get_task_assignee_deleted_task(self):
        self.task_storage.get_task.return_value = make_task(is_deleted=True)

        with pytest.raises(DeletedTaskFound):
            self.interactor.get_task_assignees(task_id="task_1")
