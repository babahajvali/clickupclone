from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    UnexpectedPermission,
)
from task_management.exceptions.enums import Permissions, Role
from task_management.interactors.dtos import (
    CreateUserSpacePermissionDTO,
    SpaceDTO,
    UserSpacePermissionDTO,
    WorkspaceMemberDTO,
)
from task_management.interactors.spaces.add_space_permission_for_user import (
    AddSpacePermissionForUser,
)
from task_management.interactors.storage_interfaces import (
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)


class InvalidPermission:
    value = "INVALID"


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


def make_user_permission() -> UserSpacePermissionDTO:
    return UserSpacePermissionDTO(
        id=1,
        space_id="space_1",
        permission_type=Permissions.FULL_EDIT,
        user_id="user_1",
        is_active=True,
        added_by="admin",
    )


class TestAddSpacePermissionForUser:
    def setup_method(self):
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = AddSpacePermissionForUser(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER):
        self.space_storage.get_space.return_value = make_space()
        self.space_storage.get_space_workspace_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )
        self.space_storage.create_user_space_permissions.return_value = [
            make_user_permission()
        ]

    def test_add_space_permission_success(self, snapshot):
        self._setup_dependencies()
        dto = CreateUserSpacePermissionDTO(
            space_id="space_1",
            user_id="user_1",
            permission_type=Permissions.FULL_EDIT,
            added_by="admin",
        )

        result = self.interactor.add_user_for_space_permission(user_data=dto)

        snapshot.assert_match(repr(result), "add_space_permission_success.txt")

    def test_add_space_permission_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)
        dto = CreateUserSpacePermissionDTO(
            space_id="space_1",
            user_id="user_1",
            permission_type=Permissions.FULL_EDIT,
            added_by="admin",
        )

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.add_user_for_space_permission(user_data=dto)

        snapshot.assert_match(
            repr(exc.value), "add_space_permission_permission_denied.txt"
        )

    def test_add_space_permission_unexpected_permission(self, snapshot):
        self._setup_dependencies()
        dto = CreateUserSpacePermissionDTO(
            space_id="space_1",
            user_id="user_1",
            permission_type=InvalidPermission,
            added_by="admin",
        )

        with pytest.raises(UnexpectedPermission) as exc:
            self.interactor.add_user_for_space_permission(user_data=dto)

        snapshot.assert_match(
            repr(exc.value), "add_space_permission_unexpected_permission.txt"
        )
