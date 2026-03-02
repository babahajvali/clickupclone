from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedTaskFound,
    TaskNotFound,
)
from task_management.interactors.storage_interfaces import TaskStorageInterface
from task_management.interactors.tasks.get_task_assignees import (
    GetTaskAssigneesInteractor,
)
from task_management.tests.interactors.task_tests.test_helpers import (
    make_task_assignee,
    make_task_data,
)


class TestGetTaskAssigneesInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.interactor = GetTaskAssigneesInteractor(task_storage=self.task_storage)

    def test_get_task_assignee_success(self, snapshot):
        self.task_storage.get_task.return_value = make_task_data()
        self.task_storage.get_task_assignees.return_value = [
            make_task_assignee(assign_id="assign_1"),
            make_task_assignee(assign_id="assign_2", user_id="user_3"),
        ]

        result = self.interactor.get_task_assignees(task_id="task_1")

        snapshot.assert_match(repr(result), "get_task_assignee_success.txt")

    def test_get_task_assignee_task_not_found(self):
        self.task_storage.get_task.return_value = None

        with pytest.raises(TaskNotFound):
            self.interactor.get_task_assignees(task_id="task_1")

    def test_get_task_assignee_deleted_task(self):
        self.task_storage.get_task.return_value = make_task_data(is_deleted=True)

        with pytest.raises(DeletedTaskFound):
            self.interactor.get_task_assignees(task_id="task_1")
