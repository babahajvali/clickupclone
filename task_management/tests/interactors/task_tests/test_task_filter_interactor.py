from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedListFound,
    InvalidLimit,
    InvalidOffset,
    ListNotFound,
)
from task_management.interactors.dtos import FilterDTO
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    TaskStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.tasks.task_filter_interactor import (
    TaskFilterInteractor,
)
from task_management.tests.interactors.task_tests.test_helpers import make_list


class TestTaskFilterInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.interactor = TaskFilterInteractor(
            task_storage=self.task_storage,
            list_storage=self.list_storage,
            workspace_storage=self.workspace_storage,
        )

    @staticmethod
    def _make_input(offset: int = 1, limit: int = 10) -> FilterDTO:
        return FilterDTO(
            list_id="list_1",
            field_filters={"priority": ["high"]},
            assignees=["user_1"],
            offset=offset,
            limit=limit,
        )

    def test_task_filter_success(self):
        filter_data = self._make_input()
        self.list_storage.get_list.return_value = make_list()
        self.task_storage.task_filter_data.return_value = ["task_1", "task_2"]

        result = self.interactor.task_filter(task_filter_data=filter_data)

        assert result == ["task_1", "task_2"]

    def test_task_filter_invalid_offset(self):
        filter_data = self._make_input(offset=0)

        with pytest.raises(InvalidOffset):
            self.interactor.task_filter(task_filter_data=filter_data)

    def test_task_filter_invalid_limit(self):
        filter_data = self._make_input(limit=0)

        with pytest.raises(InvalidLimit):
            self.interactor.task_filter(task_filter_data=filter_data)

    def test_task_filter_list_not_found(self):
        filter_data = self._make_input()
        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound):
            self.interactor.task_filter(task_filter_data=filter_data)

    def test_task_filter_deleted_list(self):
        filter_data = self._make_input()
        self.list_storage.get_list.return_value = make_list(is_deleted=True)

        with pytest.raises(DeletedListFound):
            self.interactor.task_filter(task_filter_data=filter_data)
