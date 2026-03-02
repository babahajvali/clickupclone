from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedListFound,
    EmptyTaskTitle,
    ListNotFound,
    ModificationNotAllowed,
    UserNotWorkspaceMember,
)
from task_management.exceptions.enums import Role
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    TaskStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.tasks.create_task_interactor import (
    CreateTaskInteractor,
)
from task_management.tests.interactors.task_tests.test_helpers import (
    make_create_task_input,
    make_list,
    make_permission,
    make_task,
)


class TestCreateTaskInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.interactor = CreateTaskInteractor(
            task_storage=self.task_storage,
            list_storage=self.list_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_create_task_success(self, snapshot):
        task_data = make_create_task_input()
        self.list_storage.get_list.return_value = make_list()
        self.list_storage.get_workspace_id_by_list_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission()
        self.task_storage.get_last_task_order_in_list.return_value = 2
        self.task_storage.create_task.return_value = make_task(
            title=task_data.title,
            description=task_data.description,
            list_id=task_data.list_id,
            order=3,
            created_by=task_data.created_by,
        )

        result = self.interactor.create_task(task_data=task_data)

        snapshot.assert_match(repr(result), "test_create_task_success.txt")

    def test_create_task_permission_denied(self, snapshot):
        task_data = make_create_task_input()
        self.list_storage.get_list.return_value = make_list()
        self.list_storage.get_workspace_id_by_list_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role=Role.GUEST
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_task(task_data=task_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_task_permission_denied.txt",
        )

    def test_create_task_list_not_found(self, snapshot):
        task_data = make_create_task_input()
        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound) as exc:
            self.interactor.create_task(task_data=task_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_task_list_not_found.txt",
        )

    def test_create_task_list_inactive(self, snapshot):
        task_data = make_create_task_input()
        self.list_storage.get_list.return_value = make_list(is_deleted=True)

        with pytest.raises(DeletedListFound) as exc:
            self.interactor.create_task(task_data=task_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_task_list_inactive.txt",
        )

    def test_create_task_empty_title(self):
        task_data = make_create_task_input()
        task_data.title = "   "

        with pytest.raises(EmptyTaskTitle):
            self.interactor.create_task(task_data=task_data)

    def test_create_task_user_not_workspace_member(self):
        task_data = make_create_task_input()
        self.list_storage.get_list.return_value = make_list()
        self.list_storage.get_workspace_id_by_list_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = None

        with pytest.raises(UserNotWorkspaceMember):
            self.interactor.create_task(task_data=task_data)
