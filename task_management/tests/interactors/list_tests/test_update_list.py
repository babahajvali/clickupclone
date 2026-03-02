from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    EmptyListName,
    DeletedListFound,
    ListNotFound,
    ModificationNotAllowed,
    NothingToUpdateList,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import ListDTO, WorkspaceMemberDTO
from task_management.interactors.lists.update_list_interactor import (
    UpdateListInteractor,
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


class TestUpdateList:
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
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = UpdateListInteractor(
            list_storage=self.list_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_update_list_dependencies(
            self, *, role: Role = Role.MEMBER, list_data=None
    ):
        if list_data is None:
            list_data = self._get_list_dto()

        self.list_storage.get_list.return_value = list_data
        self.list_storage.get_list_space_id.return_value = "space_1"
        self.list_storage.update_list.return_value = list_data

        self.list_storage.get_workspace_id_by_list_id.return_value = (
            "workspace_id1"
        )
        self.workspace_storage.get_workspace_member.return_value = (
            make_permission(role)
        )

    def test_update_list_success(self, snapshot):
        # Arrange
        self._setup_update_list_dependencies()

        # Act
        result = self.interactor.update_list(
            list_id="list_1",
            user_id="user_id",
            name="Updated name",
            description="Updated description",
        )

        # Assert
        snapshot.assert_match(repr(result), "update_list_success.json")
        self.list_storage.update_list.assert_called_once_with(
            list_id="list_1",
            name="Updated name",
            description="Updated description",
        )

    def test_update_list_nothing_to_update(self, snapshot):
        # Arrange
        self._setup_update_list_dependencies()

        # Act
        with pytest.raises(NothingToUpdateList) as exc:
            self.interactor.update_list(
                list_id="list_1",
                user_id="user_id",
                name=None,
                description=None,
            )

        # Assert
        snapshot.assert_match(repr(exc.value), "nothing_to_update.txt")

    def test_update_list_empty_name(self, snapshot):
        # Arrange
        self._setup_update_list_dependencies()

        # Act
        with pytest.raises(EmptyListName) as exc:
            self.interactor.update_list(
                list_id="list_1",
                user_id="user_id",
                name=" ",
                description=None,
            )

        # Assert
        snapshot.assert_match(repr(exc.value), "empty_name.txt")

    def test_update_list_not_found(self, snapshot):
        # Arrange
        self._setup_update_list_dependencies(list_data=None)
        self.list_storage.get_list.return_value = None

        # Act
        with pytest.raises(ListNotFound) as exc:
            self.interactor.update_list(
                list_id="list_1",
                user_id="user_id",
                name="Updated name",
                description=None,
            )

        # Assert
        snapshot.assert_match(repr(exc.value), "list_not_found.txt")

    def test_update_list_inactive(self, snapshot):
        # Arrange
        list_data = self._get_list_dto()
        list_data.is_deleted = True
        self._setup_update_list_dependencies(list_data=list_data)

        # Act
        with pytest.raises(DeletedListFound) as exc:
            self.interactor.update_list(
                list_id="list_1",
                user_id="user_id",
                name="Updated name",
                description=None,
            )

        # Assert
        snapshot.assert_match(repr(exc.value), "list_inactive.txt")

    def test_update_list_permission_denied(self, snapshot):
        # Arrange
        self._setup_update_list_dependencies(role=Role.GUEST)

        # Act
        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.update_list(
                list_id="list_1",
                user_id="user_id",
                name="Updated name",
                description=None,
            )

        # Assert
        snapshot.assert_match(repr(exc.value), "permission_denied.txt")
