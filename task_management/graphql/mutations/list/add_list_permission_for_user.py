import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import PermissionType
from task_management.graphql.types.error_types import (
    DeletedListType,
    ModificationNotAllowedType,
    UserNotListMemberType,
    UserHaveAlreadyListPermissionType,
)
from task_management.graphql.types.input_types import (
    AddListPermissionForUserInputParams,
)
from task_management.graphql.types.response_types import (
    AddListPermissionForUserResponse,
)
from task_management.graphql.types.types import UserListPermissionType
from task_management.interactors.dtos import CreateListPermissionDTO
from task_management.interactors.lists.create_list_permission_interactor import (
    CreateListPermissionInteractor,
)
from task_management.storages import ListStorage


class AddListPermissionForUserMutation(graphene.Mutation):
    class Arguments:
        params = AddListPermissionForUserInputParams(required=True)

    Output = AddListPermissionForUserResponse

    @staticmethod
    def mutate(root, info, params):
        added_by = info.context.user_id
        user_id = params.user_id
        permission = PermissionType(params.permission)
        list_id = params.list_id

        list_storage = ListStorage()
        interactor = CreateListPermissionInteractor(
            list_storage=list_storage,
        )

        try:
            input_data = CreateListPermissionDTO(
                list_id=list_id,
                user_id=user_id,
                permission_type=permission,
                added_by=added_by,
            )
            result = interactor.create_list_permission(
                list_permission_dto=input_data
            )

            return UserListPermissionType(
                id=result.id,
                list_id=result.list_id,
                user_id=result.user_id,
                added_by=result.added_by,
                is_active=result.is_active,
                permission_type=result.permission_type,
            )

        except custom_exceptions.ListIsDeleted as e:
            return DeletedListType(list_id=e.list_id)
        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)
        except custom_exceptions.UserNotListMember as e:
            return UserNotListMemberType(user_id=e.user_id)
        except custom_exceptions.UserAlreadyHasListPermission as e:
            return UserHaveAlreadyListPermissionType(user_id=e.user_id)
