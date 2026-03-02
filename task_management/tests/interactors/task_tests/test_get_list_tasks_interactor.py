from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedListFound,
    ListNotFound,
)
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    TaskStorageInterface,
)
from task_management.interactors.tasks.get_list_tasks_interactor import (
    GetListTasksInteractor,
)
from task_management.tests.interactors.task_tests.test_helpers import (
    make_list,
    make_task,
)


class TestGetListTasksInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.interactor = GetListTasksInteractor(
            task_storage=self.task_storage,
            list_storage=self.list_storage,
        )

    def test_get_list_tasks_success(self, snapshot):
        self.list_storage.get_list.return_value = make_list()
        self.task_storage.get_tasks_for_list.return_value = [
            make_task(task_id="task_1", order=1),
            make_task(task_id="task_2", order=2),
        ]

        result = self.interactor.get_tasks_for_list(list_id="list_1")

        snapshot.assert_match(repr(result), "test_get_list_tasks_success.txt")

    def test_get_list_tasks_list_not_found(self):
        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound):
            self.interactor.get_tasks_for_list(list_id="list_1")

    def test_get_list_tasks_deleted_list(self):
        self.list_storage.get_list.return_value = make_list(is_deleted=True)

        with pytest.raises(DeletedListFound):
            self.interactor.get_tasks_for_list(list_id="list_1")
