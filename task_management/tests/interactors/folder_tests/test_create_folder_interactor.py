from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    EmptyFolderName,
    ModificationNotAllowed,
    SpaceNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import (
    CreateFolderDTO,
    FolderDTO,
    WorkspaceMemberDTO,
)
from task_management.interactors.folders.create_folder_interactor import (
    CreateFolderInteractor,
)
from task_management.interactors.storage_interfaces import (
    FolderStorageInterface,
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)


def make_permission(role: Role) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        user_id="user_1",
        role=role,
        is_active=True,
        added_by="admin",
    )


def make_folder(order: int = 1) -> FolderDTO:
    return FolderDTO(
        folder_id="folder_1",
        name="Folder",
        description="Desc",
        space_id="space_1",
        order=order,
        is_deleted=False,
        created_by="user_1",
        is_private=False,
    )


class TestCreateFolderInteractor:
    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = CreateFolderInteractor(
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER):
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_deleted": False}
        )()
        self.space_storage.get_space_workspace_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )
        self.folder_storage.get_last_folder_order_in_space.return_value = 2
        self.folder_storage.create_folder.return_value = make_folder(order=3)

    def test_create_folder_success(self, snapshot):
        self._setup_dependencies()
        dto = CreateFolderDTO(
            name="Folder",
            description="Desc",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        result = self.interactor.create_folder(folder_data=dto)

        snapshot.assert_match(repr(result), "create_folder_success.txt")

    def test_create_folder_empty_name(self, snapshot):
        self._setup_dependencies()
        dto = CreateFolderDTO(
            name="   ",
            description="Desc",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        with pytest.raises(EmptyFolderName) as exc:
            self.interactor.create_folder(folder_data=dto)

        snapshot.assert_match(repr(exc.value), "create_folder_empty_name.txt")

    def test_create_folder_space_not_found(self, snapshot):
        self._setup_dependencies()
        self.space_storage.get_space.return_value = None
        dto = CreateFolderDTO(
            name="Folder",
            description="Desc",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        with pytest.raises(SpaceNotFound) as exc:
            self.interactor.create_folder(folder_data=dto)

        snapshot.assert_match(repr(exc.value), "create_folder_space_not_found.txt")

    def test_create_folder_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)
        dto = CreateFolderDTO(
            name="Folder",
            description="Desc",
            space_id="space_1",
            created_by="user_1",
            is_private=False,
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_folder(folder_data=dto)

        snapshot.assert_match(
            repr(exc.value), "create_folder_permission_denied.txt"
        )
