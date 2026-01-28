from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import UserNotFoundType
from task_management.graphql.types.types import WorkspaceMemberType, \
    WorkspaceMembersType

from task_management.interactors.workspace_interactors.workspace_member_interactors import \
    WorkspaceMemberInteractor
from task_management.storages.folder_permission_storage import \
    FolderPermissionStorage
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.list_permission_storage import \
    ListPermissionStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_permission_storage import \
    SpacePermissionStorage
from task_management.storages.space_storage import SpaceStorage
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_user_workspace_resolver(root, info, params):
    user_id = params.user_id

    workspace_member_storage = WorkspaceMemberStorage()
    workspace_storage = WorkspaceStorage()
    user_storage = UserStorage()
    space_permission_storage = SpacePermissionStorage()
    folder_permission_storage = FolderPermissionStorage()
    list_permission_storage = ListPermissionStorage()
    space_storage = SpaceStorage()
    folder_storage = FolderStorage()
    list_storage = ListStorage()

    interactor = WorkspaceMemberInteractor(
        workspace_member_storage=workspace_member_storage,
        workspace_storage=workspace_storage,
        user_storage=user_storage,
        space_permission_storage=space_permission_storage,
        folder_permission_storage=folder_permission_storage,
        list_permission_storage=list_permission_storage,
        space_storage=space_storage,
        folder_storage=folder_storage,
        list_storage=list_storage
    )

    try:
        workspace_data = interactor.get_user_workspaces(user_id=user_id)

        user_workspaces = [WorkspaceMemberType(
            id=result.id,
            workspace_id=result.workspace_id,
            user_id=result.user_id,
            role=result.role,
            is_active=result.is_active,
            added_by=result.added_by
        ) for result in workspace_data]

        return WorkspaceMembersType(members=user_workspaces)

    except custom_exceptions.UserNotFoundException as e:
        return UserNotFoundType(user_id=e.user_id)
