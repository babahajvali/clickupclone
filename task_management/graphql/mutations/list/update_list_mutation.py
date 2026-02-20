import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import ListNotFoundType, \
    InactiveListType, ModificationNotAllowedType, SpaceNotFoundType, \
    InactiveSpaceType, FolderNotFoundType, InactiveFolderType
from task_management.graphql.types.input_types import UpdateListInputParams
from task_management.graphql.types.response_types import UpdateListResponse
from task_management.graphql.types.types import ListType

from task_management.interactors.dtos import UpdateListDTO
from task_management.interactors.lists.list_interactor import \
    ListInteractor
from task_management.storages import ListStorage, FolderStorage, SpaceStorage, \
    WorkspaceStorage


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

        interactor = ListInteractor(
            list_storage=list_storage,
            folder_storage=folder_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage
        )

        try:
            update_list_data = UpdateListDTO(
                list_id=params.list_id,
                name=params.name if params.name else None,
                description=params.description if params.description else None
            )

            result = interactor.update_list(
                update_list_data=update_list_data,
                user_id=info.context.user_id
            )

            return ListType(
                list_id=result.list_id,
                name=result.name,
                description=result.description,
                space_id=result.space_id,
                is_active=result.is_active,
                order=result.order,
                is_private=result.is_private,
                created_by=result.created_by,
                folder_id=result.folder_id if result.folder_id else None
            )

        except custom_exceptions.ListNotFound as e:
            return ListNotFoundType(list_id=e.list_id)

        except custom_exceptions.InactiveList as e:
            return InactiveListType(list_id=e.list_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.SpaceNotFound as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.InactiveSpace as e:
            return InactiveSpaceType(space_id=e.space_id)

        except custom_exceptions.FolderNotFound as e:
            return FolderNotFoundType(folder_id=e.folder_id)

        except custom_exceptions.InactiveFolder as e:
            return InactiveFolderType(folder_id=e.folder_id)
