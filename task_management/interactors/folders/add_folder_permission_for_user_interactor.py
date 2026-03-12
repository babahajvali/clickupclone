from task_management.exceptions.custom_exceptions import UnexpectedPermission
from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import UserFolderPermissionDTO, \
    CreateFolderPermissionDTO
from task_management.interactors.storage_interfaces import FolderStorageInterface
from task_management.mixins import FolderValidationMixin


class AddFolderPermissionForUserInteractor(
    FolderValidationMixin,
):

    def __init__(
            self, folder_storage: FolderStorageInterface):
        super().__init__(
            folder_storage=folder_storage,
        )
        self.folder_storage = folder_storage

    def add_user_for_folder_permission(
            self, permission_data: CreateFolderPermissionDTO) \
            -> UserFolderPermissionDTO:
        self.check_folder_not_deleted(
            folder_id=permission_data.folder_id
        )
        self.check_user_has_edit_access_folder_permission(
            folder_id=permission_data.folder_id,
            user_id=permission_data.added_by
        )
        self._check_permission_type_is_valid(
            permission=permission_data.permission_type.value
        )

        return self.folder_storage.create_folder_users_permissions(
            users_permission_data=[permission_data])[0]

    @staticmethod
    def _check_permission_type_is_valid(permission: str):
        existed_permissions = PermissionType.get_values()
        is_invalid_permission_type = permission not in existed_permissions

        if is_invalid_permission_type:
            raise UnexpectedPermission(permission=permission)
