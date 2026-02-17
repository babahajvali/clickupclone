from django.db import transaction

from task_management.exceptions.enums import Permissions
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    CreateFolderPermissionDTO
from task_management.interactors.space.folder_interactor import \
    FolderInteractor
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface, SpaceStorageInterface, WorkspaceStorageInterface


class FolderCreationHandler:

    def __init__(self, folder_storage: FolderStorageInterface,
                 space_storage: SpaceStorageInterface,
                 workspace_storage: WorkspaceStorageInterface):
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @transaction.atomic
    def handle_folder(self, folder_data: CreateFolderDTO) -> FolderDTO:
        folder_obj = self._create_folder(folder_data=folder_data)

        self._create_folder_permission_for_user(
            folder_id=folder_obj.folder_id, user_id=folder_data.created_by)

        return folder_obj

    def _get_folder_interactor(self):
        folder_interactor = FolderInteractor(
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage)

        return folder_interactor

    def _create_folder(self, folder_data: CreateFolderDTO) -> FolderDTO:
        folder_interactor = self._get_folder_interactor()

        return folder_interactor.create_folder(create_folder_data=folder_data)

    def _create_folder_permission_for_user(self, folder_id: str, user_id: str):
        folder_interactor = self._get_folder_interactor()

        user_permission = CreateFolderPermissionDTO(
            folder_id=folder_id,
            user_id=user_id,
            permission_type=Permissions.FULL_EDIT,
            added_by=user_id)

        return folder_interactor.add_user_for_folder_permission(
            permission_data=user_permission)
