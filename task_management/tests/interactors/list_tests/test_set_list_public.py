import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    ListDeletedException,
    ListNotFound,
    ModificationNotAllowed,
)
from task_management.exceptions.enums import Role, Visibility
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


class TestSetListPublic:
    @staticmethod
    def _get_list_dto(is_private=False):
        return ListDTO(
            list_id="list_1",
            name="List name",
            description="List description",
            space_id="space_1",
            is_deleted=False,
            order=1,
            is_private=is_private,
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

    def _setup_visibility_dependencies(
            self, *, role: Role = Role.MEMBER, list_data=None
    ):
        if list_data is None:
            list_data = self._get_list_dto()

        self.list_storage.get_list.return_value = list_data
        self.list_storage.get_list_space_id.return_value = "space_1"
        self.list_storage.update_list_visibility.return_value = list_data

        self.space_storage.get_space_workspace_id.return_value = "workspace_id1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )

    def test_set_list_public_success(self, snapshot):
        # Arrange
        self._setup_visibility_dependencies()

        # Act
        result = self.interactor.set_list_visibility(
            list_id="list_1",
            visibility=Visibility.PUBLIC,
            user_id="user_id",
        )

        # Assert
        snapshot.assert_match(repr(result), "set_list_public_success.json")
        self.list_storage.update_list_visibility.assert_called_once_with(
            list_id="list_1", visibility=Visibility.PUBLIC.value
        )

    def test_set_list_public_not_found(self, snapshot):
        # Arrange
        self._setup_visibility_dependencies(list_data=None)
        self.list_storage.get_list.return_value = None

        # Act
        with pytest.raises(ListNotFound) as exc:
            self.interactor.set_list_visibility(
                list_id="list_1",
                visibility=Visibility.PUBLIC,
                user_id="user_id",
            )

        # Assert
        snapshot.assert_match(repr(exc.value), "list_not_found.txt")

    def test_set_list_public_inactive(self, snapshot):
        # Arrange
        list_data = self._get_list_dto()
        list_data.is_deleted = True
        self._setup_visibility_dependencies(list_data=list_data)

        # Act
        with pytest.raises(ListDeletedException) as exc:
            self.interactor.set_list_visibility(
                list_id="list_1",
                visibility=Visibility.PUBLIC,
                user_id="user_id",
            )

        # Assert
        snapshot.assert_match(repr(exc.value), "list_inactive.txt")

    def test_set_list_public_permission_denied(self, snapshot):
        # Arrange
        self._setup_visibility_dependencies(role=Role.GUEST)

        # Act
        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.set_list_visibility(
                list_id="list_1",
                visibility=Visibility.PUBLIC,
                user_id="user_id",
            )

        # Assert
        snapshot.assert_match(repr(exc.value), "permission_denied.txt")
