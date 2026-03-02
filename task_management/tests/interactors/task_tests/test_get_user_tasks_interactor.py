from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import InactiveUser, UserNotFound
from task_management.interactors.dtos import TaskDTO, UserTasksDTO
from task_management.interactors.storage_interfaces import (
    TaskStorageInterface,
    UserStorageInterface,
)
from task_management.interactors.tasks.get_user_tasks_interactor import (
    GetUserTasksInteractor,
)


def make_user(is_active: bool = True):
    return type("User", (), {"is_active": is_active})()


def make_user_tasks() -> UserTasksDTO:
    return UserTasksDTO(
        user_id="user_2",
        tasks=[
            TaskDTO(
                task_id="task_1",
                title="Task 1",
                description="Task 1 description",
                list_id="list_1",
                order=1,
                created_by="user_1",
                is_deleted=False,
            ),
            TaskDTO(
                task_id="task_2",
                title="Task 2",
                description="Task 2 description",
                list_id="list_1",
                order=2,
                created_by="user_1",
                is_deleted=False,
            ),
        ],
    )


class TestGetUserTasksInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.interactor = GetUserTasksInteractor(
            task_storage=self.task_storage,
            user_storage=self.user_storage,
        )

    def _setup_dependencies(self):
        self.user_storage.get_user_data.return_value = make_user()
        self.task_storage.get_user_assigned_tasks.return_value = make_user_tasks()

    def test_get_user_assigned_tasks_success(self, snapshot):
        self._setup_dependencies()

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
