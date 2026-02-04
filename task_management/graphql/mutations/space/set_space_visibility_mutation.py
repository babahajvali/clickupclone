import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import Visibility
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    InactiveSpaceType, ModificationNotAllowedType, UnsupportedVisibilityType
from task_management.graphql.types.input_types import \
    SetSpaceVisibilityInputParams
from task_management.graphql.types.response_types import \
    SetSpaceVisibilityResponse
from task_management.graphql.types.types import SpaceType
from task_management.interactors.space_interactors.space_interactors import \
    SpaceInteractor

from task_management.storages.space_storage import SpaceStorage
from task_management.storages.list_storage import ListStorage
from task_management.storages.space_permission_storage import \
    SpacePermissionStorage
from task_management.storages.workspace_member import WorkspaceMemberStorage
from task_management.storages.workspace_storage import WorkspaceStorage


class SetSpaceVisibilityMutation(graphene.Mutation):
    class Arguments:
        params = SetSpaceVisibilityInputParams(required=True)

    Output = SetSpaceVisibilityResponse

    @staticmethod
    def mutate(root, info, params):
        space_storage = SpaceStorage()
        list_storage = ListStorage()
        permission_storage = SpacePermissionStorage()
        workspace_storage = WorkspaceStorage()
        workspace_member_storage = WorkspaceMemberStorage()

        interactor = SpaceInteractor(
            space_storage=space_storage,
            list_storage=list_storage,
            permission_storage=permission_storage,
            workspace_storage=workspace_storage,
            workspace_member_storage=workspace_member_storage
        )

        try:
            visibility = Visibility(params.visibility)
        except Exception:
            return UnsupportedVisibilityType(visibility=params.visibility)

        try:
            result = interactor.set_space_visibility(
                space_id=params.space_id,
                user_id=info.context.user_id,
                visibility=visibility
            )

            return SpaceType(
                space_id=result.space_id,
                name=result.name,
                description=result.description,
                workspace_id=result.workspace_id,
                order=result.order,
                is_active=result.is_active,
                is_private=result.is_private,
                created_by=result.created_by
            )

        except custom_exceptions.SpaceNotFoundException as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.InactiveSpaceException as e:
            return InactiveSpaceType(space_id=e.space_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UnsupportedVisibilityTypeException as e:
            return UnsupportedVisibilityType(visibility=e.visibility_type)
