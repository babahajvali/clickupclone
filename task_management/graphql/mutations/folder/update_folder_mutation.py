import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FolderNotFoundType, \
    InactiveFolderType, ModificationNotAllowedType, SpaceNotFoundType, \
    InactiveSpaceType
from task_management.graphql.types.input_types import UpdateFolderInputParams
from task_management.graphql.types.response_types import UpdateFolderResponse
from task_management.graphql.types.types import FolderType

from task_management.interactors.dtos import UpdateFolderDTO
from task_management.interactors.spaces.folder_interactor import \
    FolderInteractor
from task_management.storages import FolderStorage, SpaceStorage, \
    WorkspaceStorage


class UpdateFolderMutation(graphene.Mutation):
    class Arguments:
        params = UpdateFolderInputParams(required=True)

    Output = UpdateFolderResponse

    @staticmethod
    def mutate(root, info, params):
        folder_storage = FolderStorage()
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = FolderInteractor(
            folder_storage=folder_storage,
            workspace_storage=workspace_storage,
            space_storage=space_storage
        )

        try:
            update_folder_data = UpdateFolderDTO(
                folder_id=params.folder_id,
                name=params.name if params.name else None,
                description=params.description if params.description else None
            )

            result = interactor.update_folder(
                update_folder_data=update_folder_data,
                user_id=info.context.user_id
            )

            return FolderType(
                folder_id=result.folder_id,
                name=result.name,
                description=result.description,
                space_id=result.space_id,
                order=result.order,
                is_active=result.is_active,
                created_by=result.created_by,
                is_private=result.is_private
            )

        except custom_exceptions.FolderNotFound as e:
            return FolderNotFoundType(folder_id=e.folder_id)

        except custom_exceptions.InactiveFolder as e:
            return InactiveFolderType(folder_id=e.folder_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.SpaceNotFound as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.InactiveSpace as e:
            return InactiveSpaceType(space_id=e.space_id)
