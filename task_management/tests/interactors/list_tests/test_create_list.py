import pytest
from unittest.mock import create_autospec

from task_management.exceptions.custom_exceptions import (
    EmptyName,
    FolderDeletedException,
    FolderNotFound,
    ModificationNotAllowed,
    SpaceDeletedException,
    SpaceNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import CreateListDTO, ListDTO, \
    WorkspaceMemberDTO
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


class TestCreateList:
    @staticmethod
    def _get_list_dto(*, is_private=False, folder_id=None):
        return ListDTO(
            list_id="list_1",
            name="List name",
            description="List description",
            space_id="space_1",
            is_deleted=False,
            order=1,
            is_private=is_private,
            created_by="user_id",
            folder_id=folder_id,
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

    def _setup_create_list_dependencies(
            self,
            *,
            space_exists=True,
            space_active=True,
            folder_active=True,
            folder_exists=True,
            role: Role = Role.MEMBER,
    ):
        self.space_storage.get_space.return_value = (
            type("Space", (), {"is_deleted": not space_active})()
            if space_exists else None
        )
        self.folder_storage.get_folder.return_value = (
            type("Folder", (), {"is_deleted": not folder_active})()
            if folder_exists else None
        )

        self.list_storage.get_active_lists_last_order_in_space.return_value = 1
        self.list_storage.get_active_lists_last_order_in_folder.return_value = 1
        self.list_storage.create_list.return_value = self._get_list_dto(
            folder_id="folder_1"
        )

        self.space_storage.get_space_workspace_id.return_value = "workspace_id1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )

    def test_create_list_success(self, snapshot):
        # Arrange
        self._setup_create_list_dependencies()

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id="folder_1",
        )

        # Act
        result = self.interactor.create_list(dto)

        # Assert
        snapshot.assert_match(repr(result), "create_list_success.json")
        self.list_storage.create_list.assert_called_once()

    def test_create_list_empty_name(self, snapshot):
        # Arrange
        self._setup_create_list_dependencies()

        dto = CreateListDTO(
            name=" ",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id=None,
        )

        # Act
        with pytest.raises(EmptyName) as exc:
            self.interactor.create_list(dto)

        # Assert
        snapshot.assert_match(repr(exc.value), "test_create_list_empty_name.txt")

    def test_create_list_space_not_found(self, snapshot):
        # Arrange
        self._setup_create_list_dependencies(space_exists=False)

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id=None,
        )

        # Act
        with pytest.raises(SpaceNotFound) as exc:
            self.interactor.create_list(dto)

        # Assert
        snapshot.assert_match(repr(exc.value), "space_not_found.txt")

    def test_create_list_space_inactive(self, snapshot):
        # Arrange
        self._setup_create_list_dependencies(space_active=False)

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id=None,
        )

        # Act
        with pytest.raises(SpaceDeletedException) as exc:
            self.interactor.create_list(dto)

        # Assert
        snapshot.assert_match(repr(exc.value), "space_inactive.txt")

    def test_create_list_folder_not_found(self, snapshot):
        # Arrange
        self._setup_create_list_dependencies(folder_exists=False)

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id="folder_1",
        )

        # Act
        with pytest.raises(FolderNotFound) as exc:
            self.interactor.create_list(dto)

        # Assert
        snapshot.assert_match(repr(exc.value), "folder_not_found.txt")

    def test_create_list_folder_inactive(self, snapshot):
        # Arrange
        self._setup_create_list_dependencies(folder_active=False)

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id="folder_1",
        )

        # Act
        with pytest.raises(FolderDeletedException) as exc:
            self.interactor.create_list(dto)

        # Assert
        snapshot.assert_match(repr(exc.value), "folder_inactive.txt")

    def test_create_list_permission_denied(self, snapshot):
        # Arrange
        self._setup_create_list_dependencies(role=Role.GUEST)

        dto = CreateListDTO(
            name="List name",
            description="List description",
            space_id="space_1",
            created_by="user_id",
            is_private=False,
            folder_id=None,
        )

        # Act
        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_list(dto)

        # Assert
        snapshot.assert_match(repr(exc.value), "permission_denied.txt")
