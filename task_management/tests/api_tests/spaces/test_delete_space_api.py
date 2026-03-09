from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import SpaceDTO, WorkspaceMemberDTO
from task_management.tests.api_tests.spaces import BaseDeleteSpace


def get_space_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_space"
    )


def get_space_workspace_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_space_workspace_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace_member"
    )


def delete_space_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.delete_space"
    )


def make_space() -> SpaceDTO:
    return SpaceDTO(
        space_id="space_1",
        name="Engineering",
        description="Engineering space",
        workspace_id="workspace_1",
        order=1,
        is_deleted=True,
        is_private=False,
        created_by="user_1",
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
class TestDeleteSpaceAPI(BaseDeleteSpace):
    def _setup_common(self, mocker, role=Role.MEMBER):
        get_space = get_space_mock(mocker)
        get_space.return_value = make_space()

        get_workspace_id = get_space_workspace_id_mock(mocker)
        get_workspace_id.return_value = "workspace_1"

        get_workspace_member = get_workspace_member_mock(mocker)
        get_workspace_member.return_value = make_workspace_member(role=role)

    def test_delete_space_successfully(self, snapshot, mocker):
        self._setup_common(mocker)
        delete_space = delete_space_mock(mocker)
        delete_space.return_value = make_space()

        variables = {"params": {"spaceId": "space_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_delete_space_not_found(self, snapshot, mocker):
        get_space = get_space_mock(mocker)
        get_space.return_value = None

        variables = {"params": {"spaceId": "space_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_delete_space_permission_denied(self, snapshot, mocker):
        self._setup_common(mocker, role=Role.GUEST)

        variables = {"params": {"spaceId": "space_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
