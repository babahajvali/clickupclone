from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    InactiveSpaceType
from task_management.graphql.types.types import SpaceType
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor
from task_management.storages.space_permission_storage import \
    SpacePermissionStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_space_resolver(root, info, params):
    space_id = params.space_id

    space_storage = SpaceStorage()
    permission_storage = SpacePermissionStorage()
    workspace_storage = WorkspaceStorage()
    workspace_member_storage = WorkspaceMemberStorage()

    interactor = SpaceInteractor(
        space_storage=space_storage,
        space_permission_storage=permission_storage,
        workspace_storage=workspace_storage,
        workspace_member_storage=workspace_member_storage
    )

    try:
        space_data = interactor.get_space(space_id=space_id)

        space_output = SpaceType(
            space_id=space_data.space_id,
            name=space_data.name,
            description=space_data.description,
            workspace_id=space_data.workspace_id,
            order=space_data.order,
            is_active=space_data.is_active,
            is_private=space_data.is_private,
            created_by=space_data.created_by
        )

        return space_output

    except custom_exceptions.SpaceNotFoundException as e:
        return SpaceNotFoundType(space_id=e.space_id)

    except custom_exceptions.InactiveSpaceException as e:
        return InactiveSpaceType(space_id=e.space_id)