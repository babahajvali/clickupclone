from unittest.mock import create_autospec

import pytest

from task_management.exceptions.custom_exceptions import (
    ModificationNotAllowed,
    UnsupportedVisibilityType,
)
from task_management.exceptions.enums import Role, VisibilityType
from task_management.interactors.dtos import SpaceDTO, WorkspaceMemberDTO
from task_management.interactors.spaces.set_space_visibility_interactor import (
    SetSpaceVisibilityInteractor,
)
from task_management.interactors.storage_interfaces import (
    SpaceStorageInterface,
    WorkspaceStorageInterface,
)


class InvalidVisibility:
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


class TestSetSpaceVisibilityInteractor:
    def setup_method(self):
        self.space_storage = create_autospec(SpaceStorageInterface)
        self.workspace_storage = create_autospec(WorkspaceStorageInterface)

        self.interactor = SetSpaceVisibilityInteractor(
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage,
        )

    def _setup_dependencies(self, role: Role = Role.MEMBER):
        self.space_storage.get_space.return_value = make_space()
        self.space_storage.get_space_workspace_id.return_value = "workspace_1"
        self.workspace_storage.get_workspace_member.return_value = make_permission(
            role
        )
        self.space_storage.update_space_visibility.return_value = make_space()

    def test_set_space_visibility_success(self, snapshot):
        self._setup_dependencies()

        result = self.interactor.set_space_visibility(
            space_id="space_1",
            user_id="user_1",
            visibility=VisibilityType.PRIVATE,
        )

        snapshot.assert_match(repr(result), "set_space_visibility_success.txt")

    def test_set_space_visibility_invalid_type(self, snapshot):
        self._setup_dependencies()

        with pytest.raises(UnsupportedVisibilityType) as exc:
            self.interactor.set_space_visibility(
                space_id="space_1",
                user_id="user_1",
                visibility=InvalidVisibility,
            )

        snapshot.assert_match(
            repr(exc.value), "set_space_visibility_invalid_type.txt"
        )

    def test_set_space_visibility_permission_denied(self, snapshot):
        self._setup_dependencies(role=Role.GUEST)

        with pytest.raises(ModificationNotAllowed) as exc:
            self.interactor.set_space_visibility(
                space_id="space_1",
                user_id="user_1",
                visibility=VisibilityType.PRIVATE,
            )

        snapshot.assert_match(
            repr(exc.value), "set_space_visibility_permission_denied.txt"
        )
