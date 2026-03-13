from django.db import transaction

from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    CreateFolderPermissionDTO
from task_management.interactors.folders.create_folder_interactor import \
    CreateFolderInteractor
from task_management.interactors.folders.create_folder_permission_interactor import \
    CreateFolderPermissionInteractor
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface, SpaceStorageInterface, WorkspaceStorageInterface


class FolderCreationHandler:

    def __init__(
            self, folder_storage: FolderStorageInterface,
            space_storage: SpaceStorageInterface,
            workspace_storage: WorkspaceStorageInterface):
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.workspace_storage = workspace_storage

    @transaction.atomic
    def handle_folder_creation(
            self, create_folder_dto: CreateFolderDTO) -> FolderDTO:
        folder_dto = self._create_folder(create_folder_dto=create_folder_dto)

        if folder_dto.is_private:
            self._create_folder_permission_for_user(
                folder_id=folder_dto.folder_id,
                user_id=create_folder_dto.created_by,
            )

        return folder_dto

    def _create_folder(self, create_folder_dto: CreateFolderDTO) -> FolderDTO:
        folder_interactor = CreateFolderInteractor(
            folder_storage=self.folder_storage,
            space_storage=self.space_storage,
            workspace_storage=self.workspace_storage)

        return folder_interactor.create_folder(
            create_folder_dto=create_folder_dto
        )

    def _create_folder_permission_for_user(self, folder_id: str, user_id: str):
        folder_interactor = CreateFolderPermissionInteractor(
            folder_storage=self.folder_storage
        )

        user_permission = CreateFolderPermissionDTO(
            folder_id=folder_id,
            user_id=user_id,
            permission_type=PermissionType.FULL_EDIT,
            added_by=user_id)

        return folder_interactor.create_folder_permission(
            create_folder_permission_dto=user_permission
        )
