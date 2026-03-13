from types import SimpleNamespace

import pytest

from task_management.exceptions import custom_exceptions
from task_management.interactors.dtos import WorkspaceDTO
from task_management.tests.api_tests.workspaces import BaseTransferWorkspace


def handle_workspace_transfer_mock(mocker):
    return mocker.patch(
        "task_management.interactors.workspaces.workspace_handler."
        "WorkspaceHandler.handle_workspace_transfer"
    )


def make_workspace_dto(owner_id="user_2") -> WorkspaceDTO:
    return WorkspaceDTO(
        workspace_id="workspace_1",
        name="Workspace",
        description="Main workspace",
        user_id=owner_id,
        account_id="account_1",
        is_deleted=False,
    )


@pytest.mark.django_db
class TestTransferWorkspaceAPI(BaseTransferWorkspace):
    def test_transfer_workspace_successfully(self, snapshot, mocker):
        handle_workspace_transfer_mock(
            mocker).return_value = make_workspace_dto()

        variables = {
            "params": {
                "workspaceId": "workspace_1",
                "newUserId": "user_2",
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
            custom_exceptions.WorkspaceNotFound(workspace_id="workspace_404"),
            custom_exceptions.WorkspaceIsDeleted(workspace_id="workspace_1"),
            custom_exceptions.UserNotWorkspaceOwner(user_id="user_2"),
            custom_exceptions.UserNotFound(user_id="user_2"),
            custom_exceptions.InactiveUser(user_id="user_2"),
        ],
    )
    def test_transfer_workspace_edge_cases(
            self, snapshot, mocker, raised_exception):
        handle_workspace_transfer_mock(mocker).side_effect = raised_exception

        self.execute_schema(
            query=self.QUERY,
            variables={
                "params": {
                    "workspaceId": "workspace_1",
                    "newUserId": "user_2",
                }
            },
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
