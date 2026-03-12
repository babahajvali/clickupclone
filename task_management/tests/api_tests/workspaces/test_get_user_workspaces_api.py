from types import SimpleNamespace

import pytest

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceMemberDTO
from task_management.tests.api_tests.workspaces import BaseGetUserWorkspaces


def get_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.get_user"
    )


def get_active_user_workspaces_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage."
        "WorkspaceStorage.get_active_user_workspaces"
    )


def make_user(is_active=True):
    return type("User", (), {"is_active": is_active})()


def make_workspace_member_dto() -> WorkspaceMemberDTO:
    return WorkspaceMemberDTO(
        id=1,
        workspace_id="workspace_1",
        user_id="user_1",
        role=Role.ADMIN,
        is_active=True,
        added_by="owner_1",
    )


@pytest.mark.django_db
class TestGetUserWorkspacesAPI(BaseGetUserWorkspaces):
    def test_get_user_workspaces_successfully(self, snapshot, mocker):
        get_user_mock(mocker).return_value = make_user()
        get_active_user_workspaces_mock(mocker).return_value = [
            make_workspace_member_dto()
        ]

        variables = {"params": {"userId": "user_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_user_workspaces_user_not_found(self, snapshot, mocker):
        get_user_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"userId": "user_404"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_user_workspaces_user_inactive(self, snapshot, mocker):
        get_user_mock(mocker).return_value = make_user(is_active=False)

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"userId": "user_1"}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
