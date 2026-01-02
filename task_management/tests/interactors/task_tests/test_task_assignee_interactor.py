import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.task_interactors.task_assignee_interactor import (
    TaskAssigneeInteractor
)
from task_management.interactors.storage_interface.task_storage_interface import (
    TaskStorageInterface
)
from task_management.interactors.storage_interface.task_assignee_storage_interface import (
    TaskAssigneeStorageInterface
)
from task_management.interactors.storage_interface.user_storage_interface import (
    UserStorageInterface
)
from task_management.interactors.storage_interface.list_permission_storage_interface import (
    ListPermissionStorageInterface
)
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
        self.permission_storage = create_autospec(ListPermissionStorageInterface)

        self.interactor = TaskAssigneeInteractor(
            task_storage=self.task_storage,
            task_assignee_storage=self.task_assignee_storage,
            user_storage=self.user_storage,
            permission_storage=self.permission_storage
        )

        # 👇 ValidationMixin expects this
        self.interactor.user_storage = self.user_storage

    # ---------- helpers ----------

    def _mock_active_task(self):
        return type(
            "Task",
            (),
            {
                "is_active": True,
                "list_id": "list_123"
            }
        )()

    def _mock_active_user(self):
        return type(
            "User",
            (),
            {
                "is_active": True
            }
        )()

    # ---------- ASSIGN ----------

    def test_assign_task_assignee_success(self, snapshot):
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.task_storage.get_task_by_id.return_value = self._mock_active_task()
        self.permission_storage.get_user_permission_for_list.return_value = (
            PermissionsEnum.FULL_EDIT.value
        )

        expected = TaskAssigneeDTOFactory()
        self.task_assignee_storage.assign_task_assignee.return_value = expected

        result = self.interactor.assign_task_assignee(
            task_id="task123",
            user_id="user123",
            assigned_by="admin123"
        )

        snapshot.assert_match(
            repr(result),
            "assign_task_assignee_success.txt"
        )

    def test_assign_task_assignee_permission_denied(self, snapshot):
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.task_storage.get_task_by_id.return_value = self._mock_active_task()
        self.permission_storage.get_user_permission_for_list.return_value = (
            PermissionsEnum.VIEW.value
        )

        with pytest.raises(NotAccessToModificationException) as exc:
            self.interactor.assign_task_assignee(
                task_id="task123",
                user_id="user123",
                assigned_by="user456"
            )

        snapshot.assert_match(
            repr(exc.value),
            "permission_denied.txt"
        )

    def test_assign_task_assignee_user_not_found(self, snapshot):
        self.user_storage.get_user_data.return_value = None

        with pytest.raises(UserNotFoundException) as exc:
            self.interactor.assign_task_assignee(
                task_id="task123",
                user_id="user123",
                assigned_by="admin123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "user_not_found.txt"
        )

    def test_assign_task_assignee_task_not_found(self, snapshot):
        self.user_storage.get_user_data.return_value = self._mock_active_user()
        self.task_storage.get_task_by_id.return_value = None

        with pytest.raises(TaskNotFoundException) as exc:
            self.interactor.assign_task_assignee(
                task_id="task123",
                user_id="user123",
                assigned_by="admin123"
            )

        snapshot.assert_match(
            repr(exc.value),
            "task_not_found.txt"
        )

    # ---------- REMOVE ----------

    def test_remove_task_assignee_success(self, snapshot):
        self.task_assignee_storage.check_task_assignee_exist.return_value = True

        expected = RemoveTaskAssigneeDTOFactory()
        self.task_assignee_storage.remove_task_assignee.return_value = expected

        result = self.interactor.remove_task_assignee(
            assign_id="assign123",
            removed_by="admin123"
        )

        snapshot.assert_match(
            repr(result),
            "remove_task_assignee_success.txt"
        )

    # ---------- GET ----------

    def test_get_task_assignee_success(self, snapshot):
        self.task_storage.get_task_by_id.return_value = self._mock_active_task()

        assignees = [TaskAssigneeDTOFactory(), TaskAssigneeDTOFactory()]
        self.task_assignee_storage.get_task_assignee.return_value = assignees

        result = self.interactor.get_task_assignee("task123")

        snapshot.assert_match(
            repr(result),
            "get_task_assignee_success.txt"
        )

    def test_get_user_assigned_tasks_success(self, snapshot):
        self.user_storage.get_user_data.return_value = self._mock_active_user()

        tasks = [UserTasksDTOFactory(), UserTasksDTOFactory()]
        self.task_assignee_storage.get_user_assigned_tasks.return_value = tasks

        result = self.interactor.get_user_assigned_tasks("user123")

        snapshot.assert_match(
            repr(result),
            "get_user_assigned_tasks_success.txt"
        )
