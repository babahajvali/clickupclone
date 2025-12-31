import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.task_interactors.task_interactor import CreateTaskInteractor
from task_management.interactors.storage_interface.list_storage_interface import ListStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import TaskStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import PermissionStorageInterface
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


class TestCreateTaskInteractor:

    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.permission_storage = create_autospec(PermissionStorageInterface)
        
        self.interactor = CreateTaskInteractor(
            task_storage=self.task_storage,
            list_storage=self.list_storage,
            permission_storage=self.permission_storage
        )

    def test_create_task_success(self, snapshot):
        # Arrange
        task_data = CreateTaskDTOFactory()
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.list_storage.get_list.return_value = type("List", (), {"is_active": True})()
        self.task_storage.create_task.return_value = TaskDTOFactory()

        # Act
        result = self.interactor.create_task(task_data)

        # Assert
        assert result == self.task_storage.create_task.return_value
        self.task_storage.create_task.assert_called_once_with(task_data)

    def test_create_task_permission_denied(self, snapshot):
        # Arrange
        task_data = CreateTaskDTOFactory()
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.GUEST.value

        # Act & Assert
        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.create_task(task_data)

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_create_task_list_not_found(self, snapshot):
        # Arrange
        task_data = CreateTaskDTOFactory()
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.list_storage.get_list.return_value = None

        # Act & Assert
        with pytest.raises(ListNotFoundException) as exc:
            self.interactor.create_task(task_data)

        snapshot.assert_match(repr(exc.value), "list_not_found.txt")

    def test_create_task_list_inactive(self, snapshot):
        # Arrange
        task_data = CreateTaskDTOFactory()
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.list_storage.get_list.return_value = type("List", (), {"is_active": False})()

        # Act & Assert
        with pytest.raises(InactiveListFoundException) as exc:
            self.interactor.create_task(task_data)

        snapshot.assert_match(repr(exc.value), "list_inactive.txt")

    def test_update_task_success(self, snapshot):
        # Arrange
        update_data = UpdateTaskDTOFactory()
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        self.list_storage.get_list.return_value = type("List", (), {"is_active": True})()
        self.task_storage.get_task_by_id.return_value = TaskDTOFactory()
        self.task_storage.update_task.return_value = TaskDTOFactory()

        # Act
        result = self.interactor.update_task(update_data)

        # Assert
        assert result == self.task_storage.update_task.return_value
        self.task_storage.update_task.assert_called_once_with(update_data)

    def test_get_list_tasks_success(self, snapshot):
        # Arrange
        list_id = "list123"
        expected_tasks = [TaskDTOFactory() for _ in range(3)]
        self.list_storage.get_list.return_value = type("List", (), {"is_active": True})()
        self.task_storage.get_list_tasks.return_value = expected_tasks

        # Act
        result = self.interactor.get_list_tasks(list_id)

        # Assert
        assert result == expected_tasks
        self.task_storage.get_list_tasks.assert_called_once_with(list_id)

    def test_get_task_success(self, snapshot):
        # Arrange
        task_id = "task123"
        expected_task = TaskDTOFactory()
        self.task_storage.get_task_by_id.return_value = expected_task

        # Act
        result = self.interactor.get_task(task_id)

        # Assert
        assert result == expected_task

    def test_get_task_not_found(self, snapshot):
        # Arrange
        task_id = "nonexistent_task"
        self.task_storage.get_task_by_id.return_value = None

        # Act & Assert
        with pytest.raises(TaskNotFoundException) as exc:
            self.interactor.get_task(task_id)

        snapshot.assert_match(repr(exc.value), "task_not_found.txt")
