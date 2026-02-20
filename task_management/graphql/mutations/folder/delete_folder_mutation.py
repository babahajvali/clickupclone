import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FolderNotFoundType, \
    InactiveFolderType, ModificationNotAllowedType
from task_management.graphql.types.input_types import DeleteFolderInputParams
from task_management.graphql.types.response_types import DeleteFolderResponse
from task_management.graphql.types.types import FolderType
from task_management.interactors.space.folder_interactor import \
    FolderInteractor
from task_management.storages import FolderStorage, SpaceStorage, \
    WorkspaceStorage


class DeleteFolderMutation(graphene.Mutation):
    class Arguments:
        params = DeleteFolderInputParams(required=True)

    Output = DeleteFolderResponse

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
            result = interactor.remove_folder(
                folder_id=params.folder_id,
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
