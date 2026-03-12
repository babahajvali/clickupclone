import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import VisibilityType
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    DeletedSpaceType, ModificationNotAllowedType, \
    UnsupportedVisibilityType as UnsupportedVisibilityTypeGQL, \
    UserNotWorkspaceMemberType
from task_management.graphql.types.input_types import \
    SetSpaceVisibilityInputParams
from task_management.graphql.types.response_types import \
    SetSpaceVisibilityResponse
from task_management.graphql.types.types import SpaceType
from task_management.interactors.spaces.set_space_visibility_interactor import \
    SetSpaceVisibilityInteractor
from task_management.storages import SpaceStorage, WorkspaceStorage


class SetSpaceVisibilityMutation(graphene.Mutation):
    class Arguments:
        params = SetSpaceVisibilityInputParams(required=True)

    Output = SetSpaceVisibilityResponse

    @staticmethod
    def mutate(root, info, params):
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = SetSpaceVisibilityInteractor(
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

        try:
            visibility = VisibilityType(params.visibility)
        except ValueError:
            return UnsupportedVisibilityTypeGQL(visibility=params.visibility)

        try:
            space_dto = interactor.set_space_visibility(
                space_id=params.space_id,
                user_id=info.context.user_id,
                visibility=visibility
            )

            return SpaceType(
                space_id=space_dto.space_id,
                name=space_dto.name,
                description=space_dto.description,
                workspace_id=space_dto.workspace_id,
                order=space_dto.order,
                is_deleted=space_dto.is_deleted,
                is_private=space_dto.is_private,
                created_by=getattr(
                    space_dto,
                    "created_by",
                    getattr(space_dto, "created_by_user_id", None),
                )
            )

        except custom_exceptions.SpaceNotFound as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.DeletedSpaceFound as e:
            return DeletedSpaceType(space_id=e.space_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UnsupportedVisibilityType as e:
            return UnsupportedVisibilityTypeGQL(visibility=e.visibility_type)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)
