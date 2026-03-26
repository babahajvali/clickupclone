from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ListIsDeleted,
    ListNotFound,
    ModificationNotAllowed,
    ViewNotFound,
)
from task_management.exceptions.enums import Role, ViewType
from task_management.interactors.dtos import ListViewDTO, CreateListViewDTO, \
    WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.interactors.storage_interfaces.list_storage_interface import (
    ListStorageInterface,
)
from task_management.interactors.storage_interfaces.list_view_storage_interface import (
    ListViewStorageInterface,
)
from task_management.interactors.views.create_list_view_interactor import (
    CreateListViewInteractor,
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
        self.view_storage = create_autospec(ListViewStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = CreateListViewInteractor(
            list_storage=self.list_storage,
            view_storage=self.view_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_apply_view_for_list_success(self):
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.ADMIN
        )
        self.view_storage.get_list_view.return_value = None
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()
        expected = ListViewDTO(
            id=1,
            view_name="Table",
            list_id="list_id",
            view_type=ViewType.TABLE,
            created_by="user_id",
            is_active=True,
        )
        self.view_storage.create_list_view.return_value = expected

        create_dto = CreateListViewDTO(
            view_name="Table",
            list_id="list_id",
            view_type=ViewType.TABLE,
            created_by="user_id"
        )
        result = self.interactor.create_list_view(create_dto)

        assert result == expected

    def test_apply_view_without_permission_raises_exception(self):
        self.view_storage.get_list_view.return_value = None
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.GUEST
        )

        create_dto = CreateListViewDTO(
            view_name="Table",
            list_id="list_id",
            view_type=ViewType.TABLE,
            created_by="user_id"
        )
        with pytest.raises(ModificationNotAllowed):
            self.interactor.create_list_view(create_dto)

    def test_apply_view_for_nonexistent_view_raises_exception(self):
        self.view_storage.get_list_view.return_value = None
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.ADMIN
        )
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": False}
        )()

        create_dto = CreateListViewDTO(
            view_name="Invalid",
            list_id="list_id",
            view_type=ViewType.TABLE,
            created_by="user_id"
        )

        with pytest.raises(ViewNotFound):
            self.interactor.check_view_type("INVALID_VIEW_TYPE")

    def test_apply_view_for_nonexistent_list_raises_exception(self):
        self.view_storage.get_list_view.return_value = None
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.ADMIN
        )
        self.list_storage.get_list.return_value = None

        create_dto = CreateListViewDTO(
            view_name="Table",
            list_id="list_id",
            view_type=ViewType.TABLE,
            created_by="user_id"
        )
        with pytest.raises(ListNotFound):
            self.interactor.create_list_view(create_dto)

    def test_apply_view_for_inactive_list_raises_exception(self):
        self.view_storage.get_list_view.return_value = None
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.ADMIN
        )
        self.list_storage.get_list.return_value = type(
            "List", (), {"is_deleted": True}
        )()

        create_dto = CreateListViewDTO(
            view_name="Table",
            list_id="list_id",
            view_type=ViewType.TABLE,
            created_by="user_id"
        )
        with pytest.raises(ListIsDeleted):
            self.interactor.create_list_view(create_dto)
