from task_management.exceptions.custom_exceptions import InvalidPermission
from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import UserFolderPermissionDTO, \
    CreateFolderPermissionDTO
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface
from task_management.mixins import FolderValidationMixin


class CreateFolderPermissionInteractor(
    FolderValidationMixin,
):

    def __init__(
            self, folder_storage: FolderStorageInterface):
        super().__init__(
            folder_storage=folder_storage,
        )
        self.folder_storage = folder_storage

    def create_folder_permission(
            self, create_folder_permission_dto: CreateFolderPermissionDTO) \
            -> UserFolderPermissionDTO:
        self.check_folder_not_deleted(
            folder_id=create_folder_permission_dto.folder_id
        )
        self.check_user_has_edit_access_folder_permission(
            folder_id=create_folder_permission_dto.folder_id,
            user_id=create_folder_permission_dto.added_by
        )
        self._check_permission_type_is_valid(
            permission=create_folder_permission_dto.permission_type.value
        )

        return self.folder_storage.create_folder_users_permissions(
            users_permission_data=[create_folder_permission_dto])[0]

    @staticmethod
    def _check_permission_type_is_valid(permission: str):
        existed_permissions = PermissionType.get_values()
        is_invalid_permission_type = permission not in existed_permissions

        if is_invalid_permission_type:
            raise InvalidPermission(permission=permission)
