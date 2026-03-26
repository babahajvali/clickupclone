from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import ModificationNotAllowed
from task_management.exceptions.enums import Role, ViewType
from task_management.interactors.dtos import ListViewDTO, WorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface
from task_management.interactors.storage_interfaces.list_storage_interface import (
    ListStorageInterface,
)
from task_management.interactors.storage_interfaces.list_view_storage_interface import (
    ListViewStorageInterface,
)
from task_management.interactors.views.remove_list_view_interactor import (
    RemoveListViewInteractor,
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


class TestRemoveListViewInteractor:
    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.view_storage = create_autospec(ListViewStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = RemoveListViewInteractor(
            list_storage=self.list_storage,
            view_storage=self.view_storage,
            workspace_storage=self.workspace_storage,
        )

    def test_remove_view_for_list_success(self):
        self.view_storage.is_list_view_exist.return_value = True
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.ADMIN
        )
        expected = ListViewDTO(
            id=1,
            view_name="Table",
            list_id="list_id",
            view_type=ViewType.TABLE,
            created_by="user_id",
            is_active=False,
        )
        self.view_storage.remove_list_view.return_value = expected

        result = self.interactor.remove_view_for_list(1, "user_id")

        assert result == expected

    def test_remove_view_without_permission_raises_exception(self):
        self.view_storage.is_list_view_exist.return_value = True
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            Role.GUEST
        )

        with pytest.raises(ModificationNotAllowed):
            self.interactor.remove_view_for_list(1, "user_id")
