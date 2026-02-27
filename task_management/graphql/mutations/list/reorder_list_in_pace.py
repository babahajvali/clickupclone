import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import (
    ListNotFoundType,
    DeletedListType,
    ModificationNotAllowedType,
    InvalidOrderType,
    SpaceNotFoundType,
    DeletedSpaceType,
    UserNotWorkspaceMemberType,
)
from task_management.graphql.types.input_types import (
    ReorderListInSpaceInputParams,
)
from task_management.graphql.types.response_types import (
    ReorderListInSpaceResponse,
)
from task_management.graphql.types.types import ListType
from task_management.interactors.lists.reorder_list_in_space_interactor import (
    ReorderListInSpaceInteractor,
)
from task_management.storages import (
    ListStorage,
    SpaceStorage,
    WorkspaceStorage,
)


class ReorderListInSpaceMutation(graphene.Mutation):
    class Arguments:
        params = ReorderListInSpaceInputParams(required=True)

    Output = ReorderListInSpaceResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        space_storage = SpaceStorage()

        workspace_storage = WorkspaceStorage()

        interactor = ReorderListInSpaceInteractor(
            list_storage=list_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

        try:
            result = interactor.reorder_list_in_space(
                space_id=params.space_id,
                list_id=params.list_id,
                order=params.order,
                user_id=info.context.user_id,
            )

            return ListType(
                list_id=result.list_id,
                name=result.name,
                description=result.description,
                space_id=result.space_id,
                is_active=result.is_deleted,
                order=result.order,
                is_private=result.is_private,
                created_by=result.created_by,
                folder_id=result.folder_id if result.folder_id else None,
            )

        except custom_exceptions.ListNotFound as e:
            return ListNotFoundType(list_id=e.list_id)

        except custom_exceptions.DeletedListFound as e:
            return DeletedListType(list_id=e.list_id)

        except custom_exceptions.SpaceNotFound as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.DeletedSpaceFound as e:
            return DeletedSpaceType(space_id=e.space_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.InvalidOrder as e:
            return InvalidOrderType(order=e.order)
