import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import WorkspaceNotFoundType, \
    DeletedWorkspaceType, ModificationNotAllowedType, EmptySpaceNameType, \
    UserNotWorkspaceMemberType
from task_management.graphql.types.input_types import CreateSpaceInputParams
from task_management.graphql.types.response_types import CreateSpaceResponse
from task_management.graphql.types.types import SpaceType
from task_management.interactors.dtos import CreateSpaceDTO
from task_management.interactors.spaces.space_creation_handler import \
    SpaceCreationHandler
from task_management.storages import SpaceStorage, WorkspaceStorage


class CreateSpaceMutation(graphene.Mutation):
    class Arguments:
        params = CreateSpaceInputParams(required=True)

    Output = CreateSpaceResponse

    @staticmethod
    def mutate(root, info, params):
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        space_handler = SpaceCreationHandler(
            space_storage=space_storage,
            workspace_storage=workspace_storage,
        )

        try:
            create_space_dto = CreateSpaceDTO(
                name=params.name,
                description=params.description,
                workspace_id=params.workspace_id,
                is_private=params.is_private,
                created_by=info.context.user_id
            )

            space_dto = space_handler.handle_space_creation(
                create_space_dto=create_space_dto)

            return SpaceType(
                space_id=space_dto.space_id,
                name=space_dto.name,
                description=space_dto.description,
                workspace_id=space_dto.workspace_id,
                order=space_dto.order,
                is_deleted=space_dto.is_deleted,
                is_private=space_dto.is_private,
                created_by=space_dto.created_by
            )

        except custom_exceptions.EmptySpaceName as e:
            return EmptySpaceNameType(space_name=e.space_name)

        except custom_exceptions.WorkspaceNotFound as e:
            return WorkspaceNotFoundType(workspace_id=e.workspace_id)

        except custom_exceptions.WorkspaceIsDeleted as e:
            return DeletedWorkspaceType(workspace_id=e.workspace_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)
