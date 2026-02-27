import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FolderNotFoundType, \
    DeletedFolderType, ModificationNotAllowedType, UserNotWorkspaceMemberType, \
    NothingToUpdateFolderType
from task_management.graphql.types.input_types import UpdateFolderInputParams
from task_management.graphql.types.response_types import UpdateFolderResponse
from task_management.graphql.types.types import FolderType
from task_management.interactors.folders.update_folder_interactor import \
    UpdateFolderInteractor
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

        interactor = UpdateFolderInteractor(
            folder_storage=folder_storage,
            workspace_storage=workspace_storage,
            space_storage=space_storage
        )

        try:
            folder_id = params.folder_id
            name = params.name
            description = params.description

            result = interactor.update_folder(
                folder_id=folder_id,
                name=name,
                description=description,
                user_id=info.context.user_id
            )

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

        except custom_exceptions.FolderNotFound as e:
            return FolderNotFoundType(folder_id=e.folder_id)

        except custom_exceptions.DeletedFolderException as e:
            return DeletedFolderType(folder_id=e.folder_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.NothingToUpdateFolderException as e:
            return NothingToUpdateFolderType(folder_id=e.folder_id)
