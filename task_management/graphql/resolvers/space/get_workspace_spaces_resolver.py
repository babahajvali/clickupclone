from django.core.exceptions import ObjectDoesNotExist
from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    InactiveWorkspaceType
from task_management.graphql.types.types import SpaceType, WorkspaceSpacesType
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor

from task_management.storages.space_storage import SpaceStorage
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_permission_storage import SpacePermissionStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_workspace_spaces_resolver(root, info, params):
    workspace_id = params.workspace_id

    space_storage = SpaceStorage()
    folder_storage = FolderStorage()
    list_storage = ListStorage()
    permission_storage = SpacePermissionStorage()
    workspace_storage = WorkspaceStorage()
    workspace_member_storage = WorkspaceMemberStorage()

    interactor = SpaceInteractor(
        space_storage=space_storage,
        folder_storage=folder_storage,
        list_storage=list_storage,
        permission_storage=permission_storage,
        workspace_storage=workspace_storage,
        workspace_member_storage=workspace_member_storage
    )

    try:
        spaces_data = interactor.get_workspace_spaces(workspace_id=workspace_id)

        spaces_output = [
            SpaceType(
                space_id=space.space_id,
                name=space.name,
                description=space.description,
                workspace_id=space.workspace_id,
                order=space.order,
                is_active=space.is_active,
                is_private=space.is_private,
                created_by=space.created_by
            ) for space in spaces_data
        ]

        return WorkspaceSpacesType(spaces=spaces_output)

    except custom_exceptions.WorkspaceNotFoundException as e:
        return WorkspaceNotFoundType(workspace_id=e.workspace_id)

    except custom_exceptions.InactiveWorkspaceException as e:
        return InactiveWorkspaceType(workspace_id=e.workspace_id)
