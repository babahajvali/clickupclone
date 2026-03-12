from types import SimpleNamespace
from contextlib import nullcontext

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import SpaceDTO, WorkspaceDTO, \
    WorkspaceMemberDTO
from task_management.tests.api_tests.spaces import BaseCreateSpace


def get_workspace_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def get_last_order_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_last_space_order_in_workspace"
    )


def create_space_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.create_space"
    )


def create_space_lock_mock(mocker):
    return mocker.patch(
        "task_management.interactors.spaces.create_space_interactor."
        "redis_lock",
        return_value=nullcontext(),
    )


def make_workspace(is_deleted=False) -> WorkspaceDTO:
    return WorkspaceDTO(
        workspace_id="workspace_1",
        name="Workspace",
        description="Main workspace",
        user_id="user_1",
        account_id="account_1",
        is_deleted=is_deleted,
    )


def make_workspace_member(role=Role.MEMBER) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        user_id="user_1",
        role=role,
        is_active=True,
        added_by="owner_1",
    )


def make_space(order=1) -> SpaceDTO:
    return SpaceDTO(
        space_id="space_1",
        name="Engineering",
        description="Engineering space",
        workspace_id="workspace_1",
        order=order,
        is_deleted=False,
        is_private=False,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestCreateSpaceAPI(BaseCreateSpace):
    def _setup_common(self, mocker):
        get_workspace = get_workspace_mock(mocker)
        get_workspace.return_value = make_workspace()

        get_workspace_member = get_workspace_member_mock(mocker)
        get_workspace_member.return_value = make_workspace_member()
        create_space_lock_mock(mocker)

    def test_create_space_successfully(self, snapshot, mocker):
        self._setup_common(mocker)

        last_order = get_last_order_mock(mocker)
        last_order.return_value = 1

        create_space = create_space_mock(mocker)
        create_space.return_value = make_space(order=2)

        variables = {
            "params": {
                "name": "Engineering",
                "description": "Engineering space",
                "workspaceId": "workspace_1",
                "isPrivate": False,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_space_workspace_not_found(self, snapshot, mocker):
        get_workspace = get_workspace_mock(mocker)
        get_workspace.return_value = None

        variables = {
            "params": {
                "name": "Engineering",
                "description": "Engineering space",
                "workspaceId": "workspace_404",
                "isPrivate": False,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_create_space_empty_name(self, snapshot, mocker):
        variables = {
            "params": {
                "name": "   ",
                "description": "Engineering space",
                "workspaceId": "workspace_1",
                "isPrivate": False,
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
