import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.custom_exceptions import \
    UnsupportedVisibilityType
from task_management.exceptions.enums import Visibility
from task_management.graphql.types.error_types import ListNotFoundType, \
    InactiveListType, ModificationNotAllowedType, UnsupportedVisibilityType
from task_management.graphql.types.input_types import \
    SetListVisibilityInputParams
from task_management.graphql.types.response_types import \
    SetListVisibilityResponse
from task_management.graphql.types.types import ListType
from task_management.interactors.lists.list_interactor import \
    ListInteractor
from task_management.storages import ListStorage, FolderStorage, SpaceStorage, \
    WorkspaceStorage


class SetListVisibilityMutation(graphene.Mutation):
    class Arguments:
        params = SetListVisibilityInputParams(required=True)

    Output = SetListVisibilityResponse

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
            visibility = Visibility(params.visibility)
        except UnsupportedVisibilityType as e:
            return UnsupportedVisibilityType(visibility=params.visibility)

        try:
            result = interactor.set_list_visibility(
                list_id=params.list_id,
                visibility=visibility,
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

        except custom_exceptions.UnsupportedVisibilityType as e:
            return UnsupportedVisibilityType(visibility=e.visibility_type)
