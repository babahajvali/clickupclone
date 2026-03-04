import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.custom_exceptions import (
    UnsupportedVisibilityType,
)
from task_management.exceptions.enums import VisibilityType
from task_management.graphql.types.error_types import (
    ListNotFoundType,
    DeletedListType,
    ModificationNotAllowedType,
    UnsupportedVisibilityType,
    UserNotWorkspaceMemberType,
)
from task_management.graphql.types.input_types import (
    SetListVisibilityInputParams,
)
from task_management.graphql.types.response_types import (
    SetListVisibilityResponse,
)
from task_management.graphql.types.types import ListType
from task_management.interactors.lists.set_list_visibility_interactor import (
    SetListVisibilityInteractor,
)
from task_management.storages import ListStorage, WorkspaceStorage


class SetListVisibilityMutation(graphene.Mutation):
    class Arguments:
        params = SetListVisibilityInputParams(required=True)

    Output = SetListVisibilityResponse

    @staticmethod
    def mutate(root, info, params):
        list_storage = ListStorage()
        workspace_storage = WorkspaceStorage()

        interactor = SetListVisibilityInteractor(
            list_storage=list_storage, workspace_storage=workspace_storage
        )

        try:
            visibility = VisibilityType(params.visibility)
        except UnsupportedVisibilityType as e:
            return UnsupportedVisibilityType(visibility=params.visibility)

        try:
            result = interactor.set_list_visibility(
                list_id=params.list_id,
                visibility=visibility,
                user_id=info.context.user_id,
            )

            return ListType(
                list_id=result.list_id,
                name=result.name,
                description=result.description,
                entity_type=result.entity_type.value,
                entity_id=result.entity_id,
                is_deleted=result.is_deleted,
                order=result.order,
                is_private=result.is_private,
                created_by=result.created_by,
            )

        except custom_exceptions.ListNotFound as e:
            return ListNotFoundType(list_id=e.list_id)

        except custom_exceptions.DeletedListFound as e:
            return DeletedListType(list_id=e.list_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.UnsupportedVisibilityType as e:
            return UnsupportedVisibilityType(visibility=e.visibility_type)
