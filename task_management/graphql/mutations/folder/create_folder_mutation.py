import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import SpaceNotFoundType, \
    InactiveSpaceType, ModificationNotAllowedType
from task_management.graphql.types.input_types import CreateFolderInputParams
from task_management.graphql.types.response_types import CreateFolderResponse
from task_management.graphql.types.types import FolderType

from task_management.interactors.dtos import CreateFolderDTO
from task_management.interactors.space_interactors.folders_interactor import \
    FolderInteractor
from task_management.storages.folder_storage import FolderStorage
from task_management.storages.folder_permission_storage import FolderPermissionStorage
from task_management.storages.space_permission_storage import SpacePermissionStorage
from task_management.storages.space_storage import SpaceStorage


class CreateFolderMutation(graphene.Mutation):
    class Arguments:
        params = CreateFolderInputParams(required=True)

    Output = CreateFolderResponse

    @staticmethod
    def mutate(root, info, params):
        folder_storage = FolderStorage()
        folder_permission_storage = FolderPermissionStorage()
        space_permission_storage = SpacePermissionStorage()
        space_storage = SpaceStorage()

        interactor = FolderInteractor(
            folder_storage=folder_storage,
            folder_permission_storage=folder_permission_storage,
            space_permission_storage=space_permission_storage,
            space_storage=space_storage
        )

        try:
            create_folder_data = CreateFolderDTO(
                name=params.name,
                description=params.description,
                space_id=params.space_id,
                created_by=params.created_by,
                is_private=params.is_private
            )

            result = interactor.create_folder(create_folder_data=create_folder_data)

            return FolderType(
                folder_id=str(result.folder_id),
                name=result.name,
                description=result.description,
                space_id=str(result.space_id),
                order=result.order,
                is_active=result.is_active,
                created_by=str(result.created_by),
                is_private=result.is_private
            )

        except custom_exceptions.SpaceNotFoundException as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.InactiveSpaceException as e:
            return InactiveSpaceType(space_id=e.space_id)

        except custom_exceptions.ModificationNotAllowedException as e:
            return ModificationNotAllowedType(user_id=e.user_id)