import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    DeletedSpaceType, ModificationNotAllowedType, EmptyFolderNameType, \
    UserNotWorkspaceMemberType
from task_management.graphql.types.input_types import CreateFolderInputParams
from task_management.graphql.types.response_types import CreateFolderResponse
from task_management.graphql.types.types import FolderType
from task_management.interactors.dtos import CreateFolderDTO
from task_management.interactors.folders.create_folder_interactor import \
    CreateFolderInteractor
from task_management.storages import FolderStorage, SpaceStorage, \
    WorkspaceStorage


class CreateFolderMutation(graphene.Mutation):
    class Arguments:
        params = CreateFolderInputParams(required=True)

    Output = CreateFolderResponse

    @staticmethod
    def mutate(root, info, params):
        folder_storage = FolderStorage()
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = CreateFolderInteractor(
            folder_storage=folder_storage,
            space_storage=space_storage,
            workspace_storage=workspace_storage
        )

        try:
            create_folder_data = CreateFolderDTO(
                name=params.name,
                description=params.description,
                space_id=params.space_id,
                created_by=info.context.user_id,
                is_private=params.is_private
            )

            result = interactor.create_folder(
                folder_data=create_folder_data)

            return FolderType(
                folder_id=result.folder_id,
                name=result.name,
                description=result.description,
                space_id=result.space_id,
                order=result.order,
                is_active=result.is_deleted,
                created_by=result.created_by,
                is_private=result.is_private
            )

        except custom_exceptions.EmptyFolderName as e:
            return EmptyFolderNameType(folder_name=e.folder_name)

        except custom_exceptions.SpaceNotFound as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.DeletedSpaceFound as e:
            return DeletedSpaceType(space_id=e.space_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)
