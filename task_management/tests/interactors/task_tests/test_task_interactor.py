import pytest
from unittest.mock import create_autospec

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.interactors.storage_interfaces.field_storage_interface import \
    FieldStorageInterface
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interfaces.task_field_values_storage_interface import \
    FieldValueStorageInterface
from task_management.interactors.storage_interfaces.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.task_interactors.task_interactor import \
    TaskInteractor
from task_management.interactors.storage_interfaces.list_storage_interface import (
    ListStorageInterface
)
from task_management.interactors.storage_interfaces.task_storage_interface import (
    TaskStorageInterface
)
from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowedException,
    ListNotFoundException,
    InactiveListException,
    TaskNotFoundException
)
from task_management.tests.factories.interactor_factory import (
    CreateTaskDTOFactory,
    UpdateTaskDTOFactory,
    TaskDTOFactory
)


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin"
    )



class TestCreateTaskInteractor:

    def setup_method(self):
        self.task_storage = create_autospec(TaskStorageInterface)
        self.list_storage = create_autospec(ListStorageInterface)
        self.workspace_member_storage = create_autospec(WorkspaceMemberStorageInterface)
        self.field_storage = create_autospec(FieldStorageInterface)
        self.field_value_storage = create_autospec(FieldValueStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)

        self.interactor = TaskInteractor(
            task_storage=self.task_storage,
            list_storage=self.list_storage,
            workspace_member_storage=self.workspace_member_storage,
            field_storage=self.field_storage,
            field_value_storage=self.field_value_storage,
            space_storage=self.space_storage
        )

    def test_create_task_success(self, snapshot):
        task_data = CreateTaskDTOFactory()

        self.list_storage.get_list.return_value = type(
            "List", (), {"is_active": True}
        )()
        self.workspace_member_storage.get_workspace_member.return_value = (
            make_permission(Role.MEMBER)
        )
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
        self.workspace_member_storage.get_workspace_member.return_value = (
            make_permission(Role.GUEST)
        )

        with pytest.raises(ModificationNotAllowedException) as exc:
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

        with pytest.raises(InactiveListException) as exc:
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
        self.workspace_member_storage.get_workspace_member.return_value = (
            make_permission(Role.MEMBER)
        )
        self.task_storage.update_task.return_value = TaskDTOFactory()

        result = self.interactor.update_task(update_data, user_id="user_id")

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
