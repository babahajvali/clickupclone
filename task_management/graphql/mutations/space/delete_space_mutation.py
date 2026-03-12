import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    ModificationNotAllowedType, UserNotWorkspaceMemberType
from task_management.graphql.types.input_types import DeleteSpaceInputParams
from task_management.graphql.types.response_types import DeleteSpaceResponse
from task_management.graphql.types.types import SpaceType
from task_management.interactors.spaces.delete_space_interactor import \
    DeleteSpaceInteractor
from task_management.storages import SpaceStorage, WorkspaceStorage


class DeleteSpaceMutation(graphene.Mutation):
    class Arguments:
        params = DeleteSpaceInputParams(required=True)

    Output = DeleteSpaceResponse

    @staticmethod
    def mutate(root, info, params):
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = DeleteSpaceInteractor(
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

        try:
            space_dto = interactor.delete_space(
                space_id=params.space_id,
                deleted_by=info.context.user_id
            )

            return SpaceType(
                space_id=space_dto.space_id,
                name=space_dto.name,
                description=space_dto.description,
                workspace_id=space_dto.workspace_id,
                order=space_dto.order,
                is_deleted=space_dto.is_deleted,
                is_private=space_dto.is_private,
                created_by=space_dto.created_by
            )

        except custom_exceptions.SpaceNotFound as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)
