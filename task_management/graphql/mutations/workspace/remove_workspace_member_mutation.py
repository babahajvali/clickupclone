import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import \
    ModificationNotAllowedType, WorkspaceNotFoundType, \
    InactiveWorkspaceMemberType
from task_management.graphql.types.input_types import \
    RemoveWorkspaceMemberInputParams
from task_management.graphql.types.response_types import \
    AddMemberToWorkspaceResponse
from task_management.graphql.types.types import WorkspaceMemberType
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


class RemoveMemberFromWorkspaceMutation(graphene.Mutation):
    class Arguments:
        params = RemoveWorkspaceMemberInputParams(required=True)

    Output = AddMemberToWorkspaceResponse  # Can reuse same response

    @staticmethod
    def mutate(root, info, params):
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
            result = interactor.remove_member_from_workspace(
                workspace_member_id=params.workspace_member_id,
                removed_by=params.removed_by
            )

            return WorkspaceMemberType(
                id=result.id,
                workspace_id=result.workspace_id,
                user_id=result.user_id,
                role=result.role,
                is_active=result.is_active,
                added_by=result.added_by
            )

        except custom_exceptions.InactiveWorkspaceMemberException as e:
            return InactiveWorkspaceMemberType(workspace_member_id=e.workspace_member_id)

        except custom_exceptions.WorkspaceNotFoundException as e:
            return WorkspaceNotFoundType(workspace_id=e.workspace_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)