from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    DeletedListFound,
    ListNotFound,
    ModificationNotAllowed,
    ViewNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import ListViewDTO, WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import WorkspaceStorageInterface
from task_management.interactors.storage_interfaces.list_storage_interface import (
    ListStorageInterface,
)
from task_management.interactors.storage_interfaces.view_storage_interface import (
    ViewStorageInterface,
)
from task_management.interactors.views.add_list_view_interactor import (
    AddListViewInteractor,
)


def make_permission(role: Role) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin",
    )


class TestAddListViewInteractor:
    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.view_storage = create_autospec(ViewStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = AddListViewInteractor(
            list_storage=self.list_storage,
            view_storage=self.view_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_apply_view_for_list_success(self):
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.ADMIN
        )
        self.view_storage.get_list_view.return_value = None
        self.view_storage.check_view_exists.return_value = True
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()
        expected = ListViewDTO(
            id=1,
            list_id="list_id",
            view_id="view_id",
            applied_by="user_id",
            is_active=True,
        )
        self.view_storage.apply_view_for_list.return_value = expected

        result = self.interactor.apply_view_for_list("view_id", "list_id", "user_id")

        assert result == expected

    def test_apply_view_without_permission_raises_exception(self):
        self.view_storage.get_list_view.return_value = None
        self.view_storage.check_view_exists.return_value = True
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.GUEST
        )

        with pytest.raises(ModificationNotAllowed):
            self.interactor.apply_view_for_list("view_id", "list_id", "user_id")

    def test_apply_view_for_nonexistent_view_raises_exception(self):
        self.view_storage.get_list_view.return_value = None
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.ADMIN
        )
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()
        self.view_storage.check_view_exists.return_value = False

        with pytest.raises(ViewNotFound):
            self.interactor.apply_view_for_list("view_id", "list_id", "user_id")

    def test_apply_view_for_nonexistent_list_raises_exception(self):
        self.view_storage.get_list_view.return_value = None
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.ADMIN
        )
        self.view_storage.check_view_exists.return_value = True
        self.list_storage.get_list.return_value = None

        with pytest.raises(ListNotFound):
            self.interactor.apply_view_for_list("view_id", "list_id", "user_id")

    def test_apply_view_for_inactive_list_raises_exception(self):
        self.view_storage.get_list_view.return_value = None
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.ADMIN
        )
        self.view_storage.check_view_exists.return_value = True
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": True}
        )()

        with pytest.raises(DeletedListFound):
            self.interactor.apply_view_for_list("view_id", "list_id", "user_id")
