from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedTaskFound,
    InvalidOrder,
    ModificationNotAllowed,
    TaskNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import TaskDTO, WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import (
    TaskStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.tasks.reorder_task_interactor import (
    ReorderTaskInteractor,
)


def make_task(order: int = 1, is_deleted: bool = False) -> TaskDTO:
    return TaskDTO(
        task_id="task_1",
        title="Task title",
        description="Task description",
        list_id="list_1",
        order=order,
        created_by="user_1",
        is_deleted=is_deleted,
    )


def make_permission(role: Role = Role.MEMBER) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        role=role,
        user_id="user_1",
        is_active=True,
        added_by="admin_1",
    )


class TestReorderTaskInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.interactor = ReorderTaskInteractor(
            task_storage=self.task_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(
            self, current_order: int, new_order: int,
            role: Role = Role.MEMBER, tasks_count: int = 3):
        self.task_storage.get_task.return_value = make_task(
            order=current_order)
        self.task_storage.get_tasks_count.return_value = tasks_count
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role)
        self.task_storage.reorder_task.return_value = make_task(
            order=new_order)

    def test_reorder_task_move_down_success(self):
        self._setup_dependencies(current_order=1, new_order=3)

        result = self.interactor.reorder_task(
            task_id="task_1",
            order=3,
            user_id="user_1",
        )

        self.task_storage.shift_tasks_down.assert_called_once_with(
            list_id="list_1",
            current_order=1,
            new_order=3,
        )
        assert result.order == 3

    def test_reorder_task_move_up_success(self):
        self._setup_dependencies(current_order=3, new_order=1)

        result = self.interactor.reorder_task(
            task_id="task_1",
            order=1,
            user_id="user_1",
        )

        self.task_storage.shift_tasks_up.assert_called_once_with(
            list_id="list_1",
            current_order=3,
            new_order=1,
        )
        assert result.order == 1

    def test_reorder_task_same_order_returns_original(self):
        task_data = make_task(order=2)
        self.task_storage.get_task.return_value = task_data
        self.task_storage.get_tasks_count.return_value = 3
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission()

        result = self.interactor.reorder_task(
            task_id="task_1",
            order=2,
            user_id="user_1",
        )

        self.task_storage.shift_tasks_up.assert_not_called()
        self.task_storage.shift_tasks_down.assert_not_called()
        self.task_storage.reorder_task.assert_not_called()
        assert result == task_data

    def test_reorder_task_task_not_found(self):
        self.task_storage.get_task.return_value = None

        with pytest.raises(TaskNotFound):
            self.interactor.reorder_task(
                task_id="task_1",
                order=1,
                user_id="user_1",
            )

    def test_reorder_task_deleted_task(self):
        self.task_storage.get_task.return_value = make_task(
            order=1, is_deleted=True
        )

        with pytest.raises(DeletedTaskFound):
            self.interactor.reorder_task(
                task_id="task_1",
                order=1,
                user_id="user_1",
            )

    def test_reorder_task_invalid_order_less_than_one(self):
        self.task_storage.get_task.return_value = make_task(order=1)

        with pytest.raises(InvalidOrder):
            self.interactor.reorder_task(
                task_id="task_1",
                order=0,
                user_id="user_1",
            )

    def test_reorder_task_invalid_order_greater_than_task_count(self):
        self.task_storage.get_task.return_value = make_task(order=1)
        self.task_storage.get_tasks_count.return_value = 2

        with pytest.raises(InvalidOrder):
            self.interactor.reorder_task(
                task_id="task_1",
                order=3,
                user_id="user_1",
            )

    def test_reorder_task_permission_denied(self):
        self._setup_dependencies(current_order=1, new_order=2, role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed):
            self.interactor.reorder_task(
                task_id="task_1",
                order=2,
                user_id="user_1",
            )
