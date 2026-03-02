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
from task_management.interactors.dtos import CreateTaskDTO, TaskDTO, \
    WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    TaskStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.tasks.create_task_interactor import (
    CreateTaskInteractor,
)


def make_create_task_dto(name: str = "New Task") -> CreateTaskDTO:
    return CreateTaskDTO(
        title=name,
        description="Task description",
        list_id="list_1",
        created_by="user_1",
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


def make_task(order: int = 3, title: str = "New Task") -> TaskDTO:
    return TaskDTO(
        task_id="task_1",
        title=title,
        description="Task description",
        list_id="list_1",
        order=order,
        created_by="user_1",
        is_deleted=False,
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

    def _setup_dependencies(self, role: Role = Role.MEMBER):
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()
        self.list_storage.get_workspace_id_by_list_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(role))
        self.task_storage.get_last_task_order_in_list.return_value = 2
        self.task_storage.create_task.return_value = make_task()

    def test_create_task_success(self, snapshot):
        self._setup_dependencies()
        task_data = make_create_task_dto()

        result = self.interactor.create_task(task_data=task_data)

        snapshot.assert_match(repr(result), "test_create_task_success.txt")

    def test_create_task_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)
        task_data = make_create_task_dto()

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_task(task_data=task_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_task_permission_denied.txt",
        )

    def test_create_task_list_not_found(self, snapshot):
        task_data = make_create_task_dto()
        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound) as exc:
            self.interactor.create_task(task_data=task_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_task_list_not_found.txt",
        )

    def test_create_task_list_inactive(self, snapshot):
        task_data = make_create_task_dto()
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": True}
        )()

        with pytest.raises(DeletedListFound) as exc:
            self.interactor.create_task(task_data=task_data)

        snapshot.assert_match(
            repr(exc.value),
            "test_create_task_list_inactive.txt",
        )

    def test_create_task_empty_title(self):
        task_data = make_create_task_dto(name="   ")

        with pytest.raises(EmptyTaskTitle):
            self.interactor.create_task(task_data=task_data)

    def test_create_task_user_not_workspace_member(self):
        self._setup_dependencies()
        task_data = make_create_task_dto()
        self.workspace_storage.get_workspace_member.return_value = None

        with pytest.raises(UserNotWorkspaceMember):
            self.interactor.create_task(task_data=task_data)
