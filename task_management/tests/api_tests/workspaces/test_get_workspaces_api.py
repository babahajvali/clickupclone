from types import SimpleNamespace

import pytest

from task_management.interactors.dtos import WorkspaceDTO
from task_management.tests.api_tests.workspaces import BaseGetWorkspaces


def get_workspaces_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspaces"
    )


def make_workspace_dto(workspace_id="workspace_1") -> WorkspaceDTO:
    return WorkspaceDTO(
        workspace_id=workspace_id,
        name="Workspace",
        description="Main workspace",
        user_id="user_1",
        account_id="account_1",
        is_deleted=False,
    )


@pytest.mark.django_db
class TestGetWorkspacesAPI(BaseGetWorkspaces):
    def test_get_workspaces_successfully(self, snapshot, mocker):
        get_workspaces_mock(mocker).return_value = [make_workspace_dto()]

        variables = {"params": {"workspaceIds": ["workspace_1"]}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )

    def test_get_workspaces_invalid_ids(self, snapshot, mocker):
        get_workspaces_mock(mocker).return_value = [make_workspace_dto()]

        self.execute_schema(
            query=self.QUERY,
            variables={"params": {"workspaceIds": ["workspace_1", "workspace_2"]}},
            snapshot=snapshot,
            context=SimpleNamespace(user_id="user_1"),
        )
