from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import TaskNotFound
from task_management.interactors.dtos import TaskDTO
from task_management.interactors.storage_interfaces import TaskStorageInterface
from task_management.interactors.tasks.get_task_interactor import GetTaskInteractor


def make_task() -> TaskDTO:
    return TaskDTO(
        task_id="task_1",
        title="Task Title",
        description="Task description",
        list_id="list_1",
        order=1,
        created_by="user_1",
        is_deleted=False,
    )


class TestGetTaskInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.interactor = GetTaskInteractor(task_storage=self.task_storage)

    def test_get_task_success(self, snapshot):
        self.task_storage.get_task.return_value = make_task()

        result = self.interactor.get_task(task_id="task_1")

        snapshot.assert_match(repr(result), "test_get_task_success.txt")

    def test_get_task_not_found(self, snapshot):
        self.task_storage.get_task.return_value = None

        with pytest.raises(TaskNotFound) as exc:
            self.interactor.get_task(task_id="invalid_task")

        snapshot.assert_match(repr(exc.value), "test_get_task_not_found.txt")
