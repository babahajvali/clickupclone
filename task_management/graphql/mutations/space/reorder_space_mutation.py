import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    InactiveWorkspaceType, ModificationNotAllowedType, InvalidOrderType
from task_management.graphql.types.input_types import ReorderSpaceInputParams
from task_management.graphql.types.response_types import ReorderSpaceResponse
from task_management.graphql.types.types import SpaceType
from task_management.interactors.spaces.space_interactor import \
    SpaceInteractor
from task_management.storages import SpaceStorage, WorkspaceStorage


class ReorderSpaceMutation(graphene.Mutation):
    class Arguments:
        params = ReorderSpaceInputParams(required=True)

    Output = ReorderSpaceResponse

    @staticmethod
    def mutate(root, info, params):
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = SpaceInteractor(
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

        try:
            result = interactor.reorder_space(
                workspace_id=params.workspace_id,
                space_id=params.space_id,
                order=params.order,
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
                created_by=result.created_by_user_id
            )

        except custom_exceptions.WorkspaceNotFound as e:
            return WorkspaceNotFoundType(workspace_id=e.workspace_id)

        except custom_exceptions.InactiveWorkspace as e:
            return InactiveWorkspaceType(workspace_id=e.workspace_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.InvalidOrder as e:
            return InvalidOrderType(order=e.order)
