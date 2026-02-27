import graphene

from task_management.exceptions import custom_exceptions
from task_management.graphql.types.error_types import FolderNotFoundType, \
    DeletedFolderType, ModificationNotAllowedType, InvalidOrderType, \
    UserNotWorkspaceMemberType, SpaceNotFoundType, DeletedSpaceType
from task_management.graphql.types.input_types import ReorderFolderInputParams
from task_management.graphql.types.response_types import ReorderFolderResponse
from task_management.graphql.types.types import FolderType
from task_management.interactors.folders.reorder_folder_interactor import \
    ReorderFolderInteractor
from task_management.storages import FolderStorage, SpaceStorage, \
    WorkspaceStorage


class ReorderFolderMutation(graphene.Mutation):
    class Arguments:
        params = ReorderFolderInputParams(required=True)

    Output = ReorderFolderResponse

    @staticmethod
    def mutate(root, info, params):
        folder_storage = FolderStorage()
        space_storage = SpaceStorage()
        workspace_storage = WorkspaceStorage()

        interactor = ReorderFolderInteractor(
            folder_storage=folder_storage,
            workspace_storage=workspace_storage,
            space_storage=space_storage
        )

        try:
            result = interactor.reorder_folder(
                space_id=params.space_id,
                folder_id=params.folder_id,
                user_id=info.context.user_id,
                order=params.order
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

        except custom_exceptions.InvalidOrder as e:
            return InvalidOrderType(order=e.order)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)

        except custom_exceptions.SpaceNotFound as e:
            return SpaceNotFoundType(space_id=e.space_id)

        except custom_exceptions.DeletedSpaceFound as e:
            return DeletedSpaceType(space_id=e.space_id)
