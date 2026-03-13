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
        spaces_dto = interactor.get_workspace_spaces(
            workspace_id=workspace_id)

        spaces_output = [
            SpaceType(
                space_id=space_dto.space_id,
                name=space_dto.name,
                description=space_dto.description,
                workspace_id=space_dto.workspace_id,
                order=space_dto.order,
                is_deleted=space_dto.is_deleted,
                is_private=space_dto.is_private,
                created_by=space_dto.created_by
            ) for space_dto in spaces_dto
        ]

        return WorkspaceSpacesType(spaces=spaces_output)

    except custom_exceptions.WorkspaceNotFound as e:
        return WorkspaceNotFoundType(workspace_id=e.workspace_id)

    except custom_exceptions.WorkspaceIsDeleted as e:
        return DeletedWorkspaceType(workspace_id=e.workspace_id)
