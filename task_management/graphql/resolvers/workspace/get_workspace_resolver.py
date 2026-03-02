from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    InvalidWorkspaceIdsFoundType
from task_management.graphql.types.types import WorkspaceType, WorkspacesType
from task_management.interactors.workspaces.get_workspaces_interactor import \
    WorkspaceInteractor
from task_management.storages import WorkspaceStorage


def get_workspace_resolver(root, info, params):
    workspace_ids = params.workspace_ids

    workspace_storage = WorkspaceStorage()

    interactor = WorkspaceInteractor(
        workspace_storage=workspace_storage,
    )

    try:
        workspaces_data = interactor.get_workspaces(
            workspace_ids=workspace_ids)

        workspace_output = [WorkspaceType(
            workspace_id=workspace_data.workspace_id,
            name=workspace_data.name,
            description=workspace_data.description,
            user_id=workspace_data.user_id,
            account_id=workspace_data.account_id,
            is_deleted=workspace_data.is_deleted
        ) for workspace_data in workspaces_data]

        return WorkspacesType(workspaces=workspace_output)

    except custom_exceptions.InvalidWorkspaceIdsFound as e:
        return InvalidWorkspaceIdsFoundType(workspace_ids=e.workspace_ids)
