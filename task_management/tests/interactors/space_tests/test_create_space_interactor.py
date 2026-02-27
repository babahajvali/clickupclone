from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    EmptySpaceName,
    ModificationNotAllowed,
    WorkspaceNotFound,
)
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import (
    CreateSpaceDTO,
    SpaceDTO,
    WorkspaceMemberDTO,
)
from task_management.interactors.spaces.create_space_interactor import (
    CreateSpaceInteractor,
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


class TestCreateSpaceInteractor:
    def setup_method(self):
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = CreateSpaceInteractor(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER):
        self.workspace_storage.get_workspace.return_value = type(
            "Workspace", (), {"is_deleted": False}
        )()
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )
        self.space_storage.get_last_space_order_in_workspace.return_value = 2
        self.space_storage.create_space.return_value = make_space(order=3)

    def test_create_space_success(self, snapshot):
        self._setup_dependencies()
        dto = CreateSpaceDTO(
            name="Space",
            description="Desc",
            workspace_id="workspace_1",
            is_private=False,
            created_by="user_1",
        )

        result = self.interactor.create_space(space_data=dto)

        snapshot.assert_match(repr(result), "create_space_success.txt")

    def test_create_space_empty_name(self, snapshot):
        self._setup_dependencies()
        dto = CreateSpaceDTO(
            name="  ",
            description="Desc",
            workspace_id="workspace_1",
            is_private=False,
            created_by="user_1",
        )

        with pytest.raises(EmptySpaceName) as exc:
            self.interactor.create_space(space_data=dto)

        snapshot.assert_match(repr(exc.value), "create_space_empty_name.txt")

    def test_create_space_workspace_not_found(self, snapshot):
        self._setup_dependencies()
        self.workspace_storage.get_workspace.return_value = None
        dto = CreateSpaceDTO(
            name="Space",
            description="Desc",
            workspace_id="workspace_1",
            is_private=False,
            created_by="user_1",
        )

        with pytest.raises(WorkspaceNotFound) as exc:
            self.interactor.create_space(space_data=dto)

        snapshot.assert_match(
            repr(exc.value), "create_space_workspace_not_found.txt"
        )

    def test_create_space_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)
        dto = CreateSpaceDTO(
            name="Space",
            description="Desc",
            workspace_id="workspace_1",
            is_private=False,
            created_by="user_1",
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.create_space(space_data=dto)

        snapshot.assert_match(
            repr(exc.value), "create_space_permission_denied.txt"
        )
