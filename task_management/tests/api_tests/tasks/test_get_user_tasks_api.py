from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Gender
from task_management.interactors.dtos import UserTasksDTO, TaskDTO
from task_management.tests.api_tests.tasks import BaseGetUserTasks


def get_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.get_user"
    )


def get_user_assigned_tasks_mock(mocker):
    return mocker.patch(
        "task_management.storages.task_storage.TaskStorage.get_user_assigned_tasks"
    )


def make_user(is_active: bool = True):
    return type(
        "User", (),
        {
            "is_active": is_active,
            "gender": Gender.MALE,
        },
    )()


def make_user_tasks_dto() -> UserTasksDTO:
    return UserTasksDTO(
        user_id="user_1",
        tasks=[
            TaskDTO(
                task_id="task_1",
                title="Task title",
                description="Task description",
                list_id="list_1",
                order=1,
                created_by="user_1",
                is_deleted=False,
            )
        ],
    )


@pytest.mark.django_db
class TestGetUserTasksAPI(BaseGetUserTasks):
    def test_get_user_tasks_successfully(self, snapshot, mocker):
        get_user_mock(mocker).return_value = make_user()
        get_user_assigned_tasks_mock(mocker).return_value = make_user_tasks_dto()

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"userId": "user_1"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_user_tasks_user_not_found(self, snapshot, mocker):
        get_user_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"userId": "user_404"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
