import pytest

from task_management.interactors.dtos import SpaceDTO, WorkspaceDTO
from task_management.tests.api_tests.spaces import BaseGetWorkspaceSpaces


def get_workspace_mock(mocker):
    return mocker.patch(
        "task_management.storages.workspace_storage.WorkspaceStorage.get_workspace"
    )


def get_workspace_spaces_mock(mocker):
    return mocker.patch(
        "task_management.storages.space_storage.SpaceStorage.get_workspace_spaces"
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


def make_space(space_id="space_1", order=1) -> SpaceDTO:
    return SpaceDTO(
        space_id=space_id,
        name="Engineering",
        description="Engineering space",
        workspace_id="workspace_1",
        order=order,
        is_deleted=False,
        is_private=False,
        created_by="user_1",
    )


@pytest.mark.django_db
class TestGetWorkspaceSpacesAPI(BaseGetWorkspaceSpaces):
    def test_get_workspace_spaces_successfully(self, snapshot, mocker):
        get_workspace = get_workspace_mock(mocker)
        get_workspace.return_value = make_workspace()

        get_spaces = get_workspace_spaces_mock(mocker)
        get_spaces.return_value = [
            make_space(space_id="space_1", order=1),
            make_space(space_id="space_2", order=2),
        ]

        variables = {"params": {"workspaceId": "workspace_1"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )

    def test_get_workspace_spaces_workspace_not_found(self, snapshot, mocker):
        get_workspace = get_workspace_mock(mocker)
        get_workspace.return_value = None

        variables = {"params": {"workspaceId": "workspace_404"}}

        self.execute_schema(
            query=self.QUERY,
            variables=variables,
            snapshot=snapshot,
        )
