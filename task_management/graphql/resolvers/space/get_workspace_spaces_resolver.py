from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    DeletedWorkspaceType
from task_management.graphql.types.types import SpaceType, WorkspaceSpacesType
from task_management.interactors.spaces.get_workspace_spaces_interactor import \
    GetWorkspaceSpacesInteractor
from task_management.storages import SpaceStorage, WorkspaceStorage


def get_workspace_spaces_resolver(root, info, params):
    workspace_id = params.workspace_id

    space_storage = SpaceStorage()
    workspace_storage = WorkspaceStorage()

    interactor = GetWorkspaceSpacesInteractor(
        space_storage=space_storage,
        workspace_storage=workspace_storage,
    )

    try:
        spaces_data = interactor.get_workspace_spaces(
            workspace_id=workspace_id)

        spaces_output = [
            SpaceType(
                space_id=space.space_id,
                name=space.name,
                description=space.description,
                workspace_id=space.workspace_id,
                order=space.order,
                is_deleted=space.is_deleted,
                is_private=space.is_private,
                created_by=space.created_by
            ) for space in spaces_data
        ]

        return WorkspaceSpacesType(spaces=spaces_output)

    except custom_exceptions.WorkspaceNotFound as e:
        return WorkspaceNotFoundType(workspace_id=e.workspace_id)

    except custom_exceptions.DeletedWorkspaceFound as e:
        return DeletedWorkspaceType(workspace_id=e.workspace_id)
