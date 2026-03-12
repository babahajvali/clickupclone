from types import SimpleNamespace

import pytest

from task_management.exceptions.enums import Role
from task_management.interactors.dtos import WorkspaceMemberDTO, WorkspaceDTO
from task_management.tests.api_tests.workspaces import BaseAddWorkspaceMember


def get_workspace_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace"
    )


def get_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage."
        "WorkspaceStorage.get_workspace_member"
    )


def get_user_mock(mocker):
    return mocker.patch(
        "task_management.storages.user_storage.UserStorage.get_user"
    )


def create_workspace_member_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage."
        "WorkspaceStorage.create_workspace_member"
    )


def make_workspace_dto(is_deleted=False) -> WorkspaceDTO:
    return WorkspaceDTO(
        workspace_id="workspace_1",
        name="Workspace",
        description="Main workspace",
        user_id="owner_1",
        account_id="account_1",
        is_deleted=is_deleted,
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


def make_user(is_active=True):
    return type("User", (), {"is_active": is_active})()


@pytest.mark.django_db
class TestAddWorkspaceMemberAPI(BaseAddWorkspaceMember):
    def test_add_workspace_member_successfully(self, snapshot, mocker):
        get_workspace_mock(mocker).return_value = make_workspace_dto()
        get_workspace_member_mock(mocker).return_value = make_workspace_member_dto(
            role=Role.ADMIN
        )
        get_user_mock(mocker).return_value = make_user()
        create_workspace_member_mock(mocker).return_value = (
            make_workspace_member_dto(
            role=Role.MEMBER
            )
        )

        variables = {
            "params": {
                "workspaceId": "workspace_1",
                "userId": "user_2",
                "role": "MEMBER",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_add_workspace_member_workspace_not_found(self, snapshot, mocker):
        get_workspace_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "workspaceId": "workspace_404",
                    "userId": "user_2",
                    "role": "MEMBER",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_add_workspace_member_workspace_deleted(self, snapshot, mocker):
        get_workspace_mock(mocker).return_value = make_workspace_dto(is_deleted=True)

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "workspaceId": "workspace_1",
                    "userId": "user_2",
                    "role": "MEMBER",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_add_workspace_member_user_not_found(self, snapshot, mocker):
        get_workspace_mock(mocker).return_value = make_workspace_dto()
        get_workspace_member_mock(mocker).return_value = make_workspace_member_dto(
            role=Role.ADMIN
        )
        get_user_mock(mocker).return_value = None

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "workspaceId": "workspace_1",
                    "userId": "user_404",
                    "role": "MEMBER",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_add_workspace_member_user_inactive(self, snapshot, mocker):
        get_workspace_mock(mocker).return_value = make_workspace_dto()
        get_workspace_member_mock(mocker).return_value = make_workspace_member_dto(
            role=Role.ADMIN
        )
        get_user_mock(mocker).return_value = make_user(is_active=False)

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "workspaceId": "workspace_1",
                    "userId": "user_2",
                    "role": "MEMBER",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_add_workspace_member_no_edit_access(self, snapshot, mocker):
        get_workspace_mock(mocker).return_value = make_workspace_dto()
        get_workspace_member_mock(mocker).return_value = make_workspace_member_dto(
            role=Role.GUEST
        )
        get_user_mock(mocker).return_value = make_user()

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "workspaceId": "workspace_1",
                    "userId": "user_2",
                    "role": "MEMBER",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_add_workspace_member_actor_not_member(self, snapshot, mocker):
        get_workspace_mock(mocker).return_value = make_workspace_dto()
        get_workspace_member_mock(mocker).return_value = None
        get_user_mock(mocker).return_value = make_user()

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "workspaceId": "workspace_1",
                    "userId": "user_2",
                    "role": "MEMBER",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )

    def test_add_workspace_member_invalid_role(self, snapshot, mocker):
        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "workspaceId": "workspace_1",
                    "userId": "user_2",
                    "role": "INVALID",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="owner_1"),
        )
