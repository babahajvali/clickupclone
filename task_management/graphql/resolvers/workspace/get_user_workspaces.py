from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import UserNotFoundType
from task_management.graphql.types.types import WorkspaceMemberType, \
    WorkspaceMembersType

from task_management.interactors.workspace.workspace_member_interactors import \
    WorkspaceMemberInteractor
from task_management.storages.user_storage import UserStorage
from task_management.storages.workspace_storage import WorkspaceStorage


def get_user_workspace_resolver(root, info, params):
    user_id = params.user_id

    workspace_storage = WorkspaceStorage()
    user_storage = UserStorage()

    interactor = WorkspaceMemberInteractor(
        workspace_storage=workspace_storage,
        user_storage=user_storage,
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
