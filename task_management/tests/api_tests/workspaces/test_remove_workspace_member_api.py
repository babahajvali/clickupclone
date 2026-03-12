from types import SimpleNamespace

import pytest

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.tests.api_tests.workspaces import BaseRemoveWorkspaceMember


def get_workspace_member_by_id_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage."
        "WorkspaceStorage.get_workspace_member_by_id"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage."
        "WorkspaceStorage.get_workspace_member"
    )


def remove_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage."
        "WorkspaceStorage.remove_member_from_workspace"
    )


def make_workspace_member_dto(role=Role.ADMIN) -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        user_id="user_2",
        role=role,
        is_active=True,
        added_by="owner_1",
    )


@pytest.mark.django_db
class TestRemoveWorkspaceMemberAPI(BaseRemoveWorkspaceMember):
    def test_remove_workspace_member_successfully(self, snapshot, mocker):
        get_workspace_member_by_id_mock(mocker).return_value = (
            make_workspace_member_dto()
        )
        get_workspace_member_mock(mocker).return_value = make_workspace_member_dto(
            role=Role.ADMIN
        )
        remove_member_mock(mocker).return_value = WorkspaceMemberDTO(
            id=1,
            workspace_id="workspace_1",
            user_id="user_2",
            role=Role.ADMIN,
            is_active=False,
            added_by="owner_1",
        )

        variables = {"params": {"workspaceMemberId": 1}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_remove_workspace_member_not_found(self, snapshot, mocker):
        get_workspace_member_by_id_mock(mocker).side_effect = (
            custom_exceptions.WorkspaceMemberIdNotFound(workspace_member_id=99)
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"workspaceMemberId": 99}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_remove_workspace_member_inactive(self, snapshot, mocker):
        get_workspace_member_by_id_mock(mocker).return_value = WorkspaceMemberDTO(
            id=1,
            workspace_id="workspace_1",
            user_id="user_2",
            role=Role.ADMIN,
            is_active=False,
            added_by="owner_1",
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"workspaceMemberId": 1}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_remove_workspace_member_actor_not_member(self, snapshot, mocker):
        get_workspace_member_by_id_mock(mocker).return_value = (
            make_workspace_member_dto()
        )
        get_workspace_member_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"workspaceMemberId": 1}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_remove_workspace_member_no_edit_access(self, snapshot, mocker):
        get_workspace_member_by_id_mock(mocker).return_value = (
            make_workspace_member_dto()
        )
        get_workspace_member_mock(mocker).return_value = make_workspace_member_dto(
            role=Role.GUEST
        )

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"workspaceMemberId": 1}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )
