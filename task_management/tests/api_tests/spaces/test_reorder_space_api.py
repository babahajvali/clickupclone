from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import SpaceDTO, WorkspaceDTO, \
    WorkspaceMemberDTO
from task_management.tests.api_tests.spaces import BaseReorderSpace


def get_workspace_spaces_count_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_workspace_spaces_count"
    )


def get_space_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_space"
    )


def get_workspace_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def shift_spaces_down_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.shift_spaces_down"
    )


def shift_spaces_up_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.shift_spaces_up"
    )


def update_space_order_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.update_space_order"
    )


def make_space(order=1, is_deleted=False) -> SpaceDTO:
    return SpaceDTO(
        space_id="space_1",
        name="Engineering",
        description="Engineering space",
        workspace_id="workspace_1",
        order=order,
        is_deleted=is_deleted,
        is_private=False,
        created_by="user_1",
    )


def make_workspace() -> WorkspaceDTO:
    return WorkspaceDTO(
        workspace_id="workspace_1",
        name="Workspace",
        description="Main workspace",
        user_id="user_1",
        account_id="account_1",
        is_deleted=False,
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


@pytest.mark.django_db
class TestReorderSpaceAPI(BaseReorderSpace):
    def _setup_common(self, mocker, role=Role.MEMBER):
        spaces_count = get_workspace_spaces_count_mock(mocker)
        spaces_count.return_value = 3

        get_space = get_space_mock(mocker)
        get_space.return_value = make_space(order=1, is_deleted=False)

        get_workspace = get_workspace_mock(mocker)
        get_workspace.return_value = make_workspace()

        get_workspace_member = get_workspace_member_mock(mocker)
        get_workspace_member.return_value = make_workspace_member(role=role)

    def test_reorder_space_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        shift_spaces_down_mock(mocker)
        shift_spaces_up_mock(mocker)

        update_order = update_space_order_mock(mocker)
        update_order.return_value = make_space(order=2, is_deleted=False)

        variables = {
            "params": {
                "workspaceId": "workspace_1",
                "spaceId": "space_1",
                "order": 2,
                "userId": "user_1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="different_context_user"),
        )

    def test_reorder_space_invalid_order(self, snapshot, mocker):
        self._setup_common(mocker)

        variables = {
            "params": {
                "workspaceId": "workspace_1",
                "spaceId": "space_1",
                "order": 0,
                "userId": "user_1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_reorder_space_not_found(self, snapshot, mocker):
        self._setup_common(mocker)
        get_space = get_space_mock(mocker)
        get_space.return_value = None

        variables = {
            "params": {
                "workspaceId": "workspace_1",
                "spaceId": "space_404",
                "order": 2,
                "userId": "user_1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
