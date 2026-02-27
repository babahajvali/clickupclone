from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    InvalidOrder,
    ModificationNotAllowed,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import SpaceDTO, WorkspaceMemberDTO
from task_management.interactors.spaces.reorder_space_interactor import (
    ReorderSpaceInteractor,
)
from task_management.interactors.storage_interfaces import (
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


def make_space(order: int = 1) -> SpaceDTO:
    return SpaceDTO(
        space_id="space_1",
        name="Space",
        description="Desc",
        workspace_id="workspace_1",
        order=order,
        is_deleted=False,
        is_private=False,
        created_by="user_1",
    )


class TestReorderSpaceInteractor:
    def setup_method(self):
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = ReorderSpaceInteractor(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER, order: int = 1):
        self.space_storage.get_workspace_spaces_count.return_value = 3
        self.space_storage.get_space.return_value = make_space(order=order)
        self.workspace_storage.get_workspace.return_value = type(
            "Workspace", (), {"is_deleted": False}
        )()
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )
        self.space_storage.update_space_order.return_value = make_space(order=2)

    def test_reorder_space_success(self, snapshot):
        self._setup_dependencies(order=1)

        result = self.interactor.reorder_space(
            workspace_id="workspace_1",
            space_id="space_1",
            order=2,
            user_id="user_1",
        )

        snapshot.assert_match(repr(result), "reorder_space_success.txt")

    def test_reorder_space_same_order_noop(self, snapshot):
        self._setup_dependencies(order=2)

        result = self.interactor.reorder_space(
            workspace_id="workspace_1",
            space_id="space_1",
            order=2,
            user_id="user_1",
        )

        snapshot.assert_match(repr(result), "reorder_space_same_order.txt")

    def test_reorder_space_invalid_order(self, snapshot):
        self._setup_dependencies()

        with pytest.raises(InvalidOrder) as exc:
            self.interactor.reorder_space(
                workspace_id="workspace_1",
                space_id="space_1",
                order=0,
                user_id="user_1",
            )

        snapshot.assert_match(repr(exc.value), "reorder_space_invalid_order.txt")

    def test_reorder_space_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.reorder_space(
                workspace_id="workspace_1",
                space_id="space_1",
                order=2,
                user_id="user_1",
            )

        snapshot.assert_match(
            repr(exc.value), "reorder_space_permission_denied.txt"
        )
