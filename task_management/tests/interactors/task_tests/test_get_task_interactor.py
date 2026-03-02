from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import TaskNotFound
from task_management.interactors.storage_interfaces import TaskStorageInterface
from task_management.interactors.tasks.get_task_interactor import GetTaskInteractor
from task_management.tests.interactors.task_tests.test_helpers import make_task


class TestGetTaskInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.interactor = GetTaskInteractor(task_storage=self.task_storage)

    def test_get_task_success(self, snapshot):
        self.task_storage.get_task.return_value = make_task(task_id="task_1")

        result = self.interactor.get_task(task_id="task_1")

        snapshot.assert_match(repr(result), "test_get_task_success.txt")

    def test_get_task_not_found(self, snapshot):
        self.task_storage.get_task.return_value = None

        with pytest.raises(TaskNotFound) as exc:
            self.interactor.get_task(task_id="invalid_task")

        snapshot.assert_match(repr(exc.value), "test_get_task_not_found.txt")
