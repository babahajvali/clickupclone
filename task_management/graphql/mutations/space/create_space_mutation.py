import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    InactiveWorkspaceType, ModificationNotAllowedType
from task_management.graphql.types.input_types import CreateSpaceInputParams
from task_management.graphql.types.response_types import CreateSpaceResponse
from task_management.graphql.types.types import SpaceType
from task_management.interactors.dtos import CreateSpaceDTO
from task_management.interactors.space.space_interactor import \
    SpaceInteractor
from task_management.storages import SpaceStorage, WorkspaceStorage


class CreateSpaceMutation(graphene.Mutation):
    class Arguments:
        params = CreateSpaceInputParams(required=True)

    Output = CreateSpaceResponse

    @staticmethod
    def mutate(root, info, params):
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = SpaceInteractor(
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

        try:
            create_space_data = CreateSpaceDTO(
                name=params.name,
                description=params.description,
                workspace_id=params.workspace_id,
                is_private=params.is_private,
                created_by=info.context.user_id
            )

            result = interactor.create_space(
                space_data=create_space_data)

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

        except custom_exceptions.WorkspaceNotFound as e:
            return WorkspaceNotFoundType(workspace_id=e.workspace_id)

        except custom_exceptions.InactiveWorkspace as e:
            return InactiveWorkspaceType(workspace_id=e.workspace_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)
