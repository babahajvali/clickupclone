from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedTaskFound,
    EmptyTaskTitle,
    ModificationNotAllowed,
    NothingToUpdateTask,
    TaskNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import TaskDTO, WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import (
    TaskStorageInterface,
    WorkspaceStorageInterface,
)
from task_management.interactors.tasks.update_task_interactor import (
    UpdateTaskInteractor,
)


def make_task(is_deleted: bool = False) -> TaskDTO:
    return TaskDTO(
        task_id="task_1",
        title="Task Title",
        description="Task description",
        list_id="list_1",
        order=1,
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


class TestUpdateTaskInteractor:
    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)
        self.interactor = UpdateTaskInteractor(
            task_storage=self.task_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER):
        self.task_storage.get_task.return_value = make_task()
        self.task_storage.get_workspace_id_from_task_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(role))
        self.task_storage.update_task.return_value = TaskDTO(
            task_id="task_1",
            title="Updated Task",
            description="Updated description",
            list_id="list_1",
            order=1,
            created_by="user_1",
            is_deleted=False,
        )

    def test_update_task_success(self, snapshot):
        self._setup_dependencies()

        result = self.interactor.update_task(
            task_id="task_1",
            user_id="user_1",
            title="Updated Task",
            description="Updated description",
        )

        snapshot.assert_match(repr(result), "test_update_task_success.txt")

    def test_update_task_nothing_to_update(self):
        with pytest.raises(NothingToUpdateTask):
            self.interactor.update_task(
                task_id="task_1",
                user_id="user_1",
                title=None,
                description=None,
            )

    def test_update_task_empty_title(self):
        with pytest.raises(EmptyTaskTitle):
            self.interactor.update_task(
                task_id="task_1",
                user_id="user_1",
                title="  ",
                description=None,
            )

    def test_update_task_not_found(self):
        self.task_storage.get_task.return_value = None

        with pytest.raises(TaskNotFound):
            self.interactor.update_task(
                task_id="task_1",
                user_id="user_1",
                title="Updated",
                description=None,
            )

    def test_update_task_deleted(self):
        self.task_storage.get_task.return_value = make_task(is_deleted=True)

        with pytest.raises(DeletedTaskFound):
            self.interactor.update_task(
                task_id="task_1",
                user_id="user_1",
                title="Updated",
                description=None,
            )

    def test_update_task_permission_denied(self):
        self._setup_dependencies(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed):
            self.interactor.update_task(
                task_id="task_1",
                user_id="user_1",
                title="Updated",
                description=None,
            )
