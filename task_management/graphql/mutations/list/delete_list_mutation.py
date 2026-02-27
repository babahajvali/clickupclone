import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import (
    ListNotFoundType,
    ModificationNotAllowedType,
    UserNotWorkspaceMemberType,
)
from task_management.graphql.types.input_types import DeleteListInputParams
from task_management.graphql.types.response_types import DeleteListResponse
from task_management.graphql.types.types import ListType
from task_management.interactors.lists.delete_list_interactor import (
    DeleteListInteractor,
)
from task_management.storages import (
    ListStorage,
    WorkspaceStorage,
)


class DeleteListMutation(graphene.Mutation):
    class Arguments:
        params = DeleteListInputParams(required=True)

    Output = DeleteListResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        workspace_storage = WorkspaceStorage()

        interactor = DeleteListInteractor(
            list_storage=list_storage,
            workspace_storage=workspace_storage,
        )

        try:
            result = interactor.delete_list(
                list_id=params.list_id, user_id=info.context.user_id
            )

            return ListType(
                list_id=result.list_id,
                name=result.name,
                description=result.description,
                space_id=result.space_id,
                is_deleted=result.is_deleted,
                order=result.order,
                is_private=result.is_private,
                created_by=result.created_by,
                folder_id=result.folder_id,
            )

        except custom_exceptions.ListNotFound as e:
            return ListNotFoundType(list_id=e.list_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)
