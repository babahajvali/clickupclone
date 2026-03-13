import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    DeletedSpaceType, ModificationNotAllowedType, NothingToUpdateSpaceType
from task_management.graphql.types.input_types import UpdateSpaceInputParams
from task_management.graphql.types.response_types import UpdateSpaceResponse
from task_management.graphql.types.types import SpaceType
from task_management.interactors.spaces.update_space_interactor import \
    UpdateSpaceInteractor
from task_management.storages import SpaceStorage, WorkspaceStorage


class UpdateSpaceMutation(graphene.Mutation):
    class Arguments:
        params = UpdateSpaceInputParams(required=True)

    Output = UpdateSpaceResponse

    @staticmethod
    def mutate(root, info, params):
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = UpdateSpaceInteractor(
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

        try:
            space_id = params.space_id
            name = params.name
            description = params.description

            space_dto = interactor.update_space(
                space_id=space_id,
                name=name,
                description=description,
                user_id=info.context.user_id
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

        except custom_exceptions.SpaceIsDeleted as e:
            return DeletedSpaceType(space_id=e.space_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.NothingToUpdateSpace as e:
            return NothingToUpdateSpaceType(space_id=e.space_id)
