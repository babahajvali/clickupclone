import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import UserListPermissionDTO
from task_management.interactors.task_interactors.task_interactor import TaskInteractor
from task_management.interactors.storage_interface.list_permission_storage_interface import (
    ListPermissionStorageInterface
)
from task_management.interactors.storage_interface.list_storage_interface import (
    ListStorageInterface
)
from task_management.interactors.storage_interface.task_storage_interface import (
    TaskStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    NotAccessToModificationException,
    ListNotFoundException,
    InactiveListFoundException,
    TaskNotFoundException
)
from task_management.tests.factories.interactor_factory import (
    CreateTaskDTOFactory,
    UpdateTaskDTOFactory,
    TaskDTOFactory
)

def make_permission(permission_type: PermissionsEnum):
    return UserListPermissionDTO(
        id=1,
        list_id="list_id",
        permission_type=permission_type,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )


class TestCreateTaskInteractor:

    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.permission_storage = create_autospec(ListPermissionStorageInterface)

        self.interactor = TaskInteractor(
            task_storage=self.task_storage,
            list_storage=self.list_storage,
            permission_storage=self.permission_storage
        )

    def test_create_task_success(self, snapshot):
        task_data = CreateTaskDTOFactory()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )
        self.task_storage.check_task_order_exist.return_value = False
        self.task_storage.create_task.return_value = TaskDTOFactory()

        result = self.interactor.create_task(task_data)

        snapshot.assert_match(
            repr(result),
            "test_create_task_success.txt"
        )

    def test_create_task_permission_denied(self, snapshot):
        task_data = CreateTaskDTOFactory()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.VIEW)
        )

        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.create_task(task_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_task_permission_denied.txt"
        )

    def test_create_task_list_not_found(self, snapshot):
        task_data = CreateTaskDTOFactory()

        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFoundException) as exc:
            self.interactor.create_task(task_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_task_list_not_found.txt"
        )

    def test_create_task_list_inactive(self, snapshot):
        task_data = CreateTaskDTOFactory()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": False}
        )()

        with pytest.raises(InactiveListFoundException) as exc:
            self.interactor.create_task(task_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_task_list_inactive.txt"
        )

    def test_update_task_success(self, snapshot):
        update_data = UpdateTaskDTOFactory()

        self.task_storage.get_task_by_id.return_value = TaskDTOFactory()
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.permission_storage.get_user_permission_for_list.return_value = (
            make_permission(PermissionsEnum.FULL_EDIT)
        )
        self.task_storage.check_task_order_exist.return_value = False
        self.task_storage.update_task.return_value = TaskDTOFactory()

        result = self.interactor.update_task(update_data)

        snapshot.assert_match(
            repr(result),
            "test_update_task_success.txt"
        )

    def test_get_list_tasks_success(self, snapshot):
        list_id = "list_1"
        tasks = [TaskDTOFactory(), TaskDTOFactory()]

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.task_storage.get_list_tasks.return_value = tasks

        result = self.interactor.get_list_tasks(list_id)

        snapshot.assert_match(
            repr(result),
            "test_get_list_tasks_success.txt"
        )

    def test_get_task_success(self, snapshot):
        task = TaskDTOFactory()
        self.task_storage.get_task_by_id.return_value = task

        result = self.interactor.get_task(task.task_id)

        snapshot.assert_match(
            repr(result),
            "test_get_task_success.txt"
        )

    def test_get_task_not_found(self, snapshot):
        self.task_storage.get_task_by_id.return_value = None

        with pytest.raises(TaskNotFoundException) as exc:
            self.interactor.get_task("invalid_task")

        snapshot.assert_match(
            repr(exc.value),
            "test_get_task_not_found.txt"
        )
