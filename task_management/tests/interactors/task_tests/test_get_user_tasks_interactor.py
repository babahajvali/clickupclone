from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import InactiveUser, UserNotFound
from task_management.interactors.storage_interfaces import (
    TaskStorageInterface,
    UserStorageInterface,
)
from task_management.interactors.tasks.get_user_tasks_interactor import (
    GetUserTasksInteractor,
)
from task_management.tests.interactors.task_tests.test_helpers import (
    make_user,
    make_user_tasks,
)


class TestGetUserTasksInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.interactor = GetUserTasksInteractor(
            task_storage=self.task_storage,
            user_storage=self.user_storage,
        )

    def test_get_user_assigned_tasks_success(self, snapshot):
        self.user_storage.get_user_data.return_value = make_user()
        self.task_storage.get_user_assigned_tasks.return_value = make_user_tasks()

        result = self.interactor.get_user_assigned_tasks(user_id="user_2")

        snapshot.assert_match(repr(result), "get_user_assigned_tasks_success.txt")

    def test_get_user_assigned_tasks_user_not_found(self):
        self.user_storage.get_user_data.return_value = None

        with pytest.raises(UserNotFound):
            self.interactor.get_user_assigned_tasks(user_id="user_2")

    def test_get_user_assigned_tasks_inactive_user(self):
        self.user_storage.get_user_data.return_value = make_user(is_active=False)

        with pytest.raises(InactiveUser):
            self.interactor.get_user_assigned_tasks(user_id="user_2")
