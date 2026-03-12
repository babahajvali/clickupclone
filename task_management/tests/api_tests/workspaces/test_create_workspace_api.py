from types import SimpleNamespace

import pytest

from task_management.exceptions import custom_exceptions
from task_management.interactors.dtos import WorkspaceDTO
from task_management.tests.api_tests.workspaces import BaseCreateWorkspace


def handle_workspace_creation_mock(mocker):
    return mocker.patch(
        "task_management.interactors.workspaces.workspace_handler."
        "WorkspaceHandler.handle_workspace_creation"
    )


def make_workspace_dto() -> WorkspaceDTO:
    return WorkspaceDTO(
        workspace_id="workspace_1",
        name="Workspace",
        description="Main workspace",
        user_id="user_1",
        account_id="account_1",
        is_deleted=False,
    )


@pytest.mark.django_db
class TestCreateWorkspaceAPI(BaseCreateWorkspace):
    def test_create_workspace_successfully(self, snapshot, mocker):
        handle_workspace_creation_mock(mocker).return_value = make_workspace_dto()

        variables = {
            "params": {
                "name": "Workspace",
                "description": "Main workspace",
                "accountId": "account_1",
            }
        }

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    @pytest.mark.parametrize(
        ("raised_exception", "variables"),
        [
            (
                custom_exceptions.AccountNotFound(account_id="account_404"),
                {
                    "params": {
                        "name": "Workspace",
                        "description": "Main workspace",
                        "accountId": "account_404",
                    }
                },
            ),
            (
                custom_exceptions.InactiveAccount(account_id="account_1"),
                {
                    "params": {
                        "name": "Workspace",
                        "description": "Main workspace",
                        "accountId": "account_1",
                    }
                },
            ),
            (
                custom_exceptions.UserNotAccountOwner(user_id="user_2"),
                {
                    "params": {
                        "name": "Workspace",
                        "description": "Main workspace",
                        "accountId": "account_1",
                    }
                },
            ),
            (
                custom_exceptions.EmptyWorkspaceName(workspace_name="   "),
                {
                    "params": {
                        "name": "   ",
                        "description": "Main workspace",
                        "accountId": "account_1",
                    }
                },
            ),
        ],
    )
    def test_create_workspace_edge_cases(
            self, snapshot, mocker, raised_exception, variables):
        handle_workspace_creation_mock(mocker).side_effect = raised_exception

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
