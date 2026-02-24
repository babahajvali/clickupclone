import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    DeletedListFount,
    ListNotFound,
    ModificationNotAllowed,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import ListDTO, WorkspaceMemberDTO
from task_management.interactors.lists.list_interactor import ListInteractor
from task_management.interactors.storage_interfaces import (
    ListStorageInterface,
    FolderStorageInterface,
    SpaceStorageInterface,
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
            space_id="space_1",
            is_deleted=False,
            order=1,
            is_private=False,
            created_by="user_id",
            folder_id=None,
        )

    def setup_method(self):
        self.list_storage = create_autospec(ListStorageInterface)
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = ListInteractor(
            list_storage=self.list_storage,
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_remove_list_dependencies(
            self, *, role: Role = Role.MEMBER, list_data=None
    ):
        if list_data is None:
            list_data = self._get_list_dto()

        self.list_storage.get_list.return_value = list_data
        self.list_storage.get_list_space_id.return_value = "space_1"
        self.list_storage.delete_list.return_value = list_data

        self.space_storage.get_space_workspace_id.return_value = "workspace_id1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )

    def test_remove_list_success(self, snapshot):
        # Arrange
        self._setup_remove_list_dependencies()

        # Act
        result = self.interactor.delete_list(list_id="list_1", user_id="user_id")

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

    def test_remove_list_inactive(self, snapshot):
        # Arrange
        list_data = self._get_list_dto()
        list_data.is_deleted = True
        self._setup_remove_list_dependencies(list_data=list_data)

        # Act
        with pytest.raises(DeletedListFount) as exc:
            self.interactor.delete_list(list_id="list_1", user_id="user_id")

        # Assert
        snapshot.assert_match(repr(exc.value), "list_inactive.txt")

    def test_remove_list_permission_denied(self, snapshot):
        # Arrange
        self._setup_remove_list_dependencies(role=Role.GUEST)

        # Act
        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.delete_list(list_id="list_1", user_id="user_id")

        # Assert
        snapshot.assert_match(repr(exc.value), "permission_denied.txt")
