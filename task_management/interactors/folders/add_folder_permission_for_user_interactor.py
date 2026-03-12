from task_management.interactors.dtos import UserFolderPermissionDTO, \
    CreateFolderPermissionDTO
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface, WorkspaceStorageInterface
from task_management.mixins import FolderValidationMixin, \
    WorkspaceValidationMixin


class AddFolderPermissionForUserInteractor(
    FolderValidationMixin,
    WorkspaceValidationMixin,
):

    def __init__(
            self, folder_storage: FolderStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        super().__init__(
            folder_storage=folder_storage,
            workspace_storage=workspace_storage,
        )
        self.folder_storage = folder_storage
        self.workspace_storage = workspace_storage

    def add_user_for_folder_permission(
            self, permission_data: CreateFolderPermissionDTO) \
            -> UserFolderPermissionDTO:
        self.check_folder_not_deleted(
            folder_id=permission_data.folder_id
        )
        self._check_user_has_edit_access_for_folder(
            folder_id=permission_data.folder_id,
            user_id=permission_data.user_id
        )

        return self.folder_storage.create_folder_users_permissions(
            users_permission_data=[permission_data])[0]

    def _check_user_has_edit_access_for_folder(
            self, folder_id: str, user_id: str):
        workspace_id = self.folder_storage.get_workspace_id_from_folder_id(
            folder_id=folder_id)

        self.check_user_has_edit_access_to_workspace(
            user_id=user_id, workspace_id=workspace_id
        )
