from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType
from task_management.graphql.types.types import WorkspaceType
from task_management.interactors.workspace_interactors.workspace_interactors import \
    WorkspaceInteractor
from task_management.storages.account_storage import AccountStorage
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


def get_workspace_resolver(root, info, params):
    workspace_id = params.workspace_id

    workspace_storage = WorkspaceStorage()
    user_storage = UserStorage()
    account_storage = AccountStorage()
    workspace_member_storage = WorkspaceMemberStorage()
    space_storage = SpaceStorage()
    space_permission_storage = SpacePermissionStorage()
    folder_storage = FolderStorage()
    folder_permission_storage = FolderPermissionStorage()
    list_storage = ListStorage()
    list_permission_storage = ListPermissionStorage()

    interactor = WorkspaceInteractor(
        workspace_storage=workspace_storage,
        user_storage=user_storage,
        account_storage=account_storage,
        workspace_member_storage=workspace_member_storage,
        space_storage=space_storage,
        space_permission_storage=space_permission_storage,
        list_storage=list_storage,
        list_permission_storage=list_permission_storage,
        folder_storage=folder_storage,
        folder_permission_storage=folder_permission_storage,
    )

    try:
        workspace_data = interactor.get_workspace(workspace_id=workspace_id)

        workspace_output = WorkspaceType(
            workspace_id=workspace_data.workspace_id,
            name=workspace_data.name,
            description=workspace_data.description,
            user_id=workspace_data.user_id,
            account_id=workspace_data.account_id,
            is_active=workspace_data.is_active
        )

        return workspace_output

    except custom_exceptions.WorkspaceNotFoundException as e:
        return WorkspaceNotFoundType(workspace_id=e.workspace_id)
