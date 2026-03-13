import graphene

from task_management.exceptions import custom_exceptions
from task_management.exceptions.enums import VisibilityType
from task_management.graphql.types.error_types import FolderNotFoundType, \
    DeletedFolderType, ModificationNotAllowedType, UnsupportedVisibilityType, \
    UserNotWorkspaceMemberType
from task_management.graphql.types.input_types import \
    SetFolderVisibilityInputParams
from task_management.graphql.types.response_types import \
    SetFolderVisibilityResponse
from task_management.graphql.types.types import FolderType
from task_management.interactors.folders.set_folder_visibility_interactor import \
    SetFolderVisibilityInteractor
from task_management.storages import FolderStorage, WorkspaceStorage


class SetFolderVisibilityMutation(graphene.Mutation):
    class Arguments:
        params = SetFolderVisibilityInputParams(required=True)

    Output = SetFolderVisibilityResponse

    @staticmethod
    def mutate(root, info, params):
        folder_storage = FolderStorage()
        workspace_storage = WorkspaceStorage()

        interactor = SetFolderVisibilityInteractor(
            folder_storage=folder_storage,
            workspace_storage=workspace_storage
        )

        try:
            visibility = VisibilityType(params.visibility)
        except Exception:
            return UnsupportedVisibilityType(visibility=params.visibility)

        try:
            folder_dto = interactor.set_folder_visibility(
                folder_id=params.folder_id,
                user_id=info.context.user_id,
                visibility=visibility
            )

            return FolderType(
                folder_id=folder_dto.folder_id,
                name=folder_dto.name,
                description=folder_dto.description,
                space_id=folder_dto.space_id,
                order=folder_dto.order,
                is_deleted=folder_dto.is_deleted,
                created_by=folder_dto.created_by,
                is_private=folder_dto.is_private
            )

        except custom_exceptions.FolderNotFound as e:
            return FolderNotFoundType(folder_id=e.folder_id)

        except custom_exceptions.FolderIsDeleted as e:
            return DeletedFolderType(folder_id=e.folder_id)

        except custom_exceptions.ModificationNotAllowed as e:
            return ModificationNotAllowedType(user_id=e.user_id)

        except custom_exceptions.UnsupportedVisibilityType as e:
            return UnsupportedVisibilityType(visibility=e.visibility_type)

        except custom_exceptions.UserNotWorkspaceMember as e:
            return UserNotWorkspaceMemberType(user_id=e.user_id)
