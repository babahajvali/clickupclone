import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import (
    ListNotFoundType,
    DeletedListType,
    ModificationNotAllowedType,
    UserNotWorkspaceMemberType,
    NothingToUpdateListType,
)
from task_management.graphql.types.input_types import UpdateListInputParams
from task_management.graphql.types.response_types import UpdateListResponse
from task_management.graphql.types.types import ListType
from task_management.interactors.lists.update_list_interactor import (
    UpdateListInteractor,
)
from task_management.storages import (
    ListStorage,
    FolderStorage,
    SpaceStorage,
    WorkspaceStorage,
)


class UpdateListMutation(graphene.Mutation):
    class Arguments:
        params = UpdateListInputParams(required=True)

    Output = UpdateListResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        folder_storage = FolderStorage()
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = UpdateListInteractor(
            list_storage=list_storage,
            folder_storage=folder_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

        try:
            list_id = params.list_id
            name = params.name
            description = params.description

            result = interactor.update_list(
                list_id=list_id,
                user_id=info.context.user_id,
                name=name,
                description=description,
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
                folder_id=result.folder_id if result.folder_id else None,
            )

        except custom_exceptions.ListNotFound as e:
            return ListNotFoundType(list_id=e.list_id)

        except custom_exceptions.DeletedListFound as e:
            return DeletedListType(list_id=e.list_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.NothingToUpdateList as e:
            return NothingToUpdateListType(list_id=e.list_id)
