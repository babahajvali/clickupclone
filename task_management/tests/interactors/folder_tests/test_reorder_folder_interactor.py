from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    InvalidOrder,
    ModificationNotAllowed,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import FolderDTO, WorkspaceMemberDTO
from task_management.interactors.folders.reorder_folder_interactor import (
    ReorderFolderInteractor,
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


class TestReorderFolderInteractor:
    def setup_method(self):
        self.folder_storage = create_autospec(FolderStorageInterface)
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = ReorderFolderInteractor(
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER, order: int = 1):
        self.folder_storage.get_space_folder_count.return_value = 3
        self.folder_storage.get_folder.return_value = make_folder(order=order)
        self.space_storage.get_space.return_value = type(
            "Space", (), {"is_deleted": False}
        )()
        self.space_storage.get_space_workspace_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )
        self.folder_storage.update_folder_order.return_value = make_folder(order=2)

    def test_reorder_folder_success(self, snapshot):
        self._setup_dependencies(order=1)

        result = self.interactor.reorder_folder(
            space_id="space_1",
            folder_id="folder_1",
            user_id="user_1",
            order=2,
        )

        snapshot.assert_match(repr(result), "reorder_folder_success.txt")

    def test_reorder_folder_same_order_noop(self, snapshot):
        self._setup_dependencies(order=2)

        result = self.interactor.reorder_folder(
            space_id="space_1",
            folder_id="folder_1",
            user_id="user_1",
            order=2,
        )

        snapshot.assert_match(repr(result), "reorder_folder_same_order.txt")

    def test_reorder_folder_invalid_order(self, snapshot):
        self._setup_dependencies()

        with pytest.raises(InvalidOrder) as exc:
            self.interactor.reorder_folder(
                space_id="space_1",
                folder_id="folder_1",
                user_id="user_1",
                order=0,
            )

        snapshot.assert_match(repr(exc.value), "reorder_folder_invalid_order.txt")

    def test_reorder_folder_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.reorder_folder(
                space_id="space_1",
                folder_id="folder_1",
                user_id="user_1",
                order=2,
            )

        snapshot.assert_match(
            repr(exc.value), "reorder_folder_permission_denied.txt"
        )
