import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    DeletedWorkspaceType, ModificationNotAllowedType, InvalidOrderType, \
    SpaceNotFoundType, UserNotWorkspaceMemberType, DeletedSpaceType
from task_management.graphql.types.input_types import ReorderSpaceInputParams
from task_management.graphql.types.response_types import ReorderSpaceResponse
from task_management.graphql.types.types import SpaceType
from task_management.interactors.spaces.reorder_space_interactor import \
    ReorderSpaceInteractor
from task_management.storages import SpaceStorage, WorkspaceStorage


class ReorderSpaceMutation(graphene.Mutation):
    class Arguments:
        params = ReorderSpaceInputParams(required=True)

    Output = ReorderSpaceResponse

    @staticmethod
    def mutate(root, info, params):
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = ReorderSpaceInteractor(
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
                is_deleted=result.is_deleted,
                is_private=result.is_private,
                created_by=result.created_by
            )

        except custom_exceptions.SpaceNotFound as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.DeletedSpaceFound as e:
            return DeletedSpaceType(space_id=e.space_id)

        except custom_exceptions.WorkspaceNotFound as e:
            return WorkspaceNotFoundType(workspace_id=e.workspace_id)

        except custom_exceptions.DeletedWorkspaceFound as e:
            return DeletedWorkspaceType(workspace_id=e.workspace_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.InvalidOrder as e:
            return InvalidOrderType(order=e.order)
