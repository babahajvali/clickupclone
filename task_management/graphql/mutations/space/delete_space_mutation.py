import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    InactiveSpaceType, ModificationNotAllowedType
from task_management.graphql.types.input_types import DeleteSpaceInputParams
from task_management.graphql.types.response_types import DeleteSpaceResponse
from task_management.graphql.types.types import SpaceType
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor

from task_management.storages.space_storage import SpaceStorage
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_permission_storage import SpacePermissionStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


class DeleteSpaceMutation(graphene.Mutation):
    class Arguments:
        params = DeleteSpaceInputParams(required=True)

    Output = DeleteSpaceResponse

    @staticmethod
    def mutate(root, info, params):
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
            result = interactor.delete_space(
                space_id=params.space_id,
                user_id=params.user_id
            )

            return SpaceType(
                space_id=result.space_id,
                name=result.name,
                description=result.description,
                workspace_id=result.workspace_id,
                order=result.order,
                is_active=result.is_active,
                is_private=result.is_private,
                created_by=result.created_by
            )

        except custom_exceptions.SpaceNotFoundException as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.InactiveSpaceException as e:
            return InactiveSpaceType(space_id=e.space_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)
