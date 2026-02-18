import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import Permissions
from task_management.graphql.types.error_types import InactiveListType, \
    ModificationNotAllowedType, UserHaveAlreadyListPermissionType
from task_management.graphql.types.input_types import \
    AddListPermissionForUserInputParams
from task_management.graphql.types.response_types import \
    AddListPermissionForUserResponse
from task_management.graphql.types.types import UserListPermissionType
from task_management.interactors.dtos import CreateListPermissionDTO
from task_management.interactors.list.list_interactor import ListInteractor
from task_management.storages import ListStorage, FolderStorage, SpaceStorage, \
    WorkspaceStorage


class AddListPermissionForUserMutation(graphene.Mutation):
    class Arguments:
        params = AddListPermissionForUserInputParams(required=True)

    Output = AddListPermissionForUserResponse

    @staticmethod
    def mutate(root, info, params):
        added_by = info.context.user_id
        user_id = params.user_id
        permission = Permissions(params.permission)
        list_id = params.list_id

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
            input_data = CreateListPermissionDTO(
                list_id=list_id,
                user_id=user_id,
                permission_type=permission,
                added_by=added_by,
            )
            result = interactor.add_user_in_list_permission(
                user_permission_data=input_data)

            return UserListPermissionType(
                id=result.id,
                list_id=result.list_id,
                user_id=result.user_id,
                added_by=result.added_by,
                is_active=result.is_active,
                permission_type=result.permission_type
            )

        except custom_exceptions.InactiveListException as e:
            return InactiveListType(list_id=e.list_id)
        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)
        except custom_exceptions.UserHaveAlreadyListPermissionException as e:
            return UserHaveAlreadyListPermissionType(user_id=e.user_id)
