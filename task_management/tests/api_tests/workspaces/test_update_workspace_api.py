from types import SimpleNamespace

import pytest

from task_management.exceptions import custom_exceptions
from task_management.interactors.dtos import WorkspaceDTO
from task_management.tests.api_tests.workspaces import BaseUpdateWorkspace


def get_workspace_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace"
    )


def validate_workspace_owner_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage."
        "WorkspaceStorage.validate_user_is_workspace_owner"
    )


def update_workspace_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.update_workspace"
    )


def make_workspace_dto(is_deleted=False) -> WorkspaceDTO:
    return WorkspaceDTO(
        workspace_id="workspace_1",
        name="Workspace",
        description="Main workspace",
        user_id="user_1",
        account_id="account_1",
        is_deleted=is_deleted,
    )


@pytest.mark.django_db
class TestUpdateWorkspaceAPI(BaseUpdateWorkspace):
    def test_update_workspace_successfully(self, snapshot, mocker):
        get_workspace_mock(mocker).return_value = make_workspace_dto()
        validate_workspace_owner_mock(mocker).return_value = True
        update_workspace_mock(mocker).return_value = WorkspaceDTO(
            workspace_id="workspace_1",
            name="Updated Workspace",
            description="Updated description",
            user_id="user_1",
            account_id="account_1",
            is_deleted=False,
        )

        variables = {
            "params": {
                "workspaceId": "workspace_1",
                "name": "Updated Workspace",
                "description": "Updated description",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_update_workspace_not_found(self, snapshot, mocker):
        get_workspace_mock(mocker).return_value = None

        variables = {
            "params": {
                "workspaceId": "workspace_404",
                "name": "Updated Workspace",
                "description": "Updated description",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    @pytest.mark.parametrize(
        "raised_exception",
        [
            custom_exceptions.WorkspaceIsDeleted(workspace_id="workspace_1"),
            custom_exceptions.UserNotWorkspaceOwner(user_id="user_2"),
        ],
    )
    def test_update_workspace_edge_cases(
            self, snapshot, mocker, raised_exception):
        if isinstance(raised_exception, custom_exceptions.WorkspaceIsDeleted):
            get_workspace_mock(mocker).return_value = make_workspace_dto(
                is_deleted=True
            )
        else:
            get_workspace_mock(mocker).return_value = make_workspace_dto()
            validate_workspace_owner_mock(mocker).return_value = False

        variables = {
            "params": {
                "workspaceId": "workspace_1",
                "name": "Updated Workspace",
                "description": "Updated description",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
