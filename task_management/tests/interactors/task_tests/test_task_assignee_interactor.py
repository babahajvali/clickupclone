import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.task_interactors.task_assignee_interactor import TaskAssigneeInteractor
from task_management.interactors.storage_interface.task_storage_interface import TaskStorageInterface
from task_management.interactors.storage_interface.task_assignee_storage_interface import TaskAssigneeStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import UserStorageInterface
from task_management.interactors.storage_interface.permission_storage_interface import PermissionStorageInterface
from task_management.exceptions.custom_exceptions import (
    NotAccessToModificationException,
    TaskNotFoundException,
    UserNotFoundException
)
from task_management.tests.factories.interactor_factory import (
    TaskAssigneeDTOFactory,
    RemoveTaskAssigneeDTOFactory,
    UserTasksDTOFactory
)


class TestTaskAssigneeInteractor:

    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.task_assignee_storage = create_autospec(TaskAssigneeStorageInterface)
        self.user_storage = create_autospec(UserStorageInterface)
        self.permission_storage = create_autospec(PermissionStorageInterface)
        
        self.interactor = TaskAssigneeInteractor(
            task_storage=self.task_storage,
            task_assignee_storage=self.task_assignee_storage,
            user_storage=self.user_storage,
            permission_storage=self.permission_storage
        )

    def test_assign_task_assignee_success(self, snapshot):
        # Arrange
        task_id = "task123"
        user_id = "user123"
        assigned_by = "admin123"
        
        mock_task = type('Task', (), {'is_active': True})
        
        self.user_storage.check_user_exists.return_value = True
        self.task_storage.get_task_by_id.return_value = mock_task
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        
        expected_result = TaskAssigneeDTOFactory()
        self.task_assignee_storage.assign_task_assignee.return_value = expected_result

        # Act
        result = self.interactor.assign_task_assignee(
            task_id=task_id,
            user_id=user_id,
            assigned_by=assigned_by
        )

        # Assert
        assert result == expected_result
        self.task_assignee_storage.assign_task_assignee.assert_called_once_with(
            task_id=task_id,
            user_id=user_id,
            assigned_by=assigned_by
        )

    def test_assign_task_assignee_user_not_found(self, snapshot):
        # Arrange
        task_id = "task123"
        user_id = "nonexistent_user"
        assigned_by = "admin123"
        
        self.user_storage.check_user_exists.return_value = False

        # Act & Assert
        with pytest.raises(UserNotFoundException) as exc:
            self.interactor.assign_task_assignee(task_id, user_id, assigned_by)

        snapshot.assert_match(repr(exc.value), "user_not_found.txt")

    def test_assign_task_assignee_task_not_found(self, snapshot):
        # Arrange
        task_id = "nonexistent_task"
        user_id = "user123"
        assigned_by = "admin123"
        
        self.user_storage.check_user_exists.return_value = True
        self.task_storage.get_task_by_id.return_value = None

        # Act & Assert
        with pytest.raises(TaskNotFoundException) as exc:
            self.interactor.assign_task_assignee(task_id, user_id, assigned_by)

        snapshot.assert_match(repr(exc.value), "task_not_found.txt")

    def test_assign_task_assignee_permission_denied(self, snapshot):
        # Arrange
        task_id = "task123"
        user_id = "user123"
        assigned_by = "user456"
        
        mock_task = type('Task', (), {'is_active': True})
        
        self.user_storage.check_user_exists.return_value = True
        self.task_storage.get_task_by_id.return_value = mock_task
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.GUEST.value

        # Act & Assert
        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.assign_task_assignee(task_id, user_id, assigned_by)

        snapshot.assert_match(repr(exc.value), "permission_denied.txt")

    def test_remove_task_assignee_success(self, snapshot):
        # Arrange
        assign_id = "assign123"
        removed_by = "admin123"
        
        self.task_assignee_storage.check_task_assignee_exist.return_value = True
        self.permission_storage.get_user_access_permissions.return_value = PermissionsEnum.ADMIN.value
        
        expected_result = RemoveTaskAssigneeDTOFactory()
        self.task_assignee_storage.remove_task_assignee.return_value = expected_result

        # Act
        result = self.interactor.remove_task_assignee(assign_id, removed_by)

        # Assert
        assert result == expected_result
        self.task_assignee_storage.remove_task_assignee.assert_called_once_with(
            assign_id=assign_id,
            removed_by=removed_by
        )

    def test_get_task_assignee_success(self, snapshot):
        # Arrange
        task_id = "task123"
        expected_assignees = [TaskAssigneeDTOFactory() for _ in range(2)]
        
        mock_task = type('Task', (), {'is_active': True})
        
        self.task_storage.get_task_by_id.return_value = mock_task
        self.task_assignee_storage.get_task_assignee.return_value = expected_assignees

        # Act
        result = self.interactor.get_task_assignee(task_id)

        # Assert
        assert result == expected_assignees
        self.task_assignee_storage.get_task_assignee.assert_called_once_with(task_id)

    def test_get_user_assigned_tasks_success(self, snapshot):
        # Arrange
        user_id = "user123"
        expected_tasks = [UserTasksDTOFactory() for _ in range(2)]
        
        self.user_storage.check_user_exists.return_value = True
        self.task_assignee_storage.get_user_assigned_tasks.return_value = expected_tasks

        # Act
        result = self.interactor.get_user_assigned_tasks(user_id)

        # Assert
        assert result == expected_tasks
        self.task_assignee_storage.get_user_assigned_tasks.assert_called_once_with(user_id)
