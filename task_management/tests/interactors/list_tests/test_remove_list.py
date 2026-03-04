from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ListNotFound,
    ModificationNotAllowed,
)
from task_management.exceptions.enums import Role, ListEntityType
from task_management.interactors.dtos import ListDTO, WorkspaceMemberDTO
from task_management.interactors.lists.delete_list_interactor import (
    DeleteListInteractor,
)
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    WorkspaceStorageInterface,
)


def make_permission(role: Role):
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_id1",
        role=role,
        user_id="user_id",
        is_active=True,
        added_by="admin",
    )


class TestRemoveList:
    @staticmethod
    def _get_list_dto():
        return ListDTO(
            list_id="list_1",
            name="List name",
            description="List description",
            is_deleted=False,
            order=1,
            is_private=False,
            created_by="user_id",
            entity_type=ListEntityType.SPACE,
            entity_id="space_1",
        )

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = DeleteListInteractor(
            list_storage=self.list_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_remove_list_dependencies(
        self, *, role: Role = Role.MEMBER, list_data=None
    ):
        if list_data is None:
            list_data = self._get_list_dto()

        self.list_storage.get_list.return_value = list_data
        self.list_storage.get_workspace_id_by_list_id.return_value = "workspace_id1"
        self.list_storage.delete_list.return_value = list_data
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(role)
        )

    def test_remove_list_success(self, snapshot):
        # Arrange
        self._setup_remove_list_dependencies()

        # Act
        result = self.interactor.delete_list(
            list_id="list_1", user_id="user_id"
        )

        # Assert
        snapshot.assert_match(repr(result), "remove_list_success.json")
        self.list_storage.delete_list.assert_called_once_with(list_id="list_1")

    def test_remove_list_not_found(self, snapshot):
        # Arrange
        self._setup_remove_list_dependencies(list_data=None)
        self.list_storage.get_list.return_value = None

        # Act
        with pytest.raises(ListNotFound) as exc:
            self.interactor.delete_list(list_id="list_1", user_id="user_id")

        # Assert
        snapshot.assert_match(repr(exc.value), "list_not_found.txt")

    def test_remove_list_permission_denied(self, snapshot):
        # Arrange
        self._setup_remove_list_dependencies(role=Role.GUEST)

        # Act
        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.delete_list(list_id="list_1", user_id="user_id")

        # Assert
        snapshot.assert_match(repr(exc.value), "permission_denied.txt")
