from task_management.exceptions.custom_exceptions import \
    FolderNotFound, FolderIsDeleted, EmptyFolderName, \
    ModificationNotAllowed, UserNotFolderMember
from task_management.exceptions.enums import PermissionType
from task_management.interactors.dtos import FolderDTO
from task_management.interactors.storage_interfaces import \
    FolderStorageInterface


class FolderValidationMixin:

    def __init__(self, folder_storage: FolderStorageInterface, **kwargs):
        self.folder_storage = folder_storage
        super().__init__(**kwargs)

    def check_folder_not_deleted(self, folder_id: str):
        folder_dto = self.check_folder_exists(folder_id=folder_id)

        is_folder_delete = folder_dto.is_deleted
        if is_folder_delete:
            raise FolderIsDeleted(folder_id=folder_id)

    def check_folder_exists(self, folder_id: str) -> FolderDTO:

        folder_dto = self.folder_storage.get_folder(
            folder_id=folder_id)

        if not folder_dto:
            raise FolderNotFound(folder_id=folder_id)

        return folder_dto

    @staticmethod
    def check_folder_name_not_empty(name: str):
        is_name_empty = name is None or not name.strip()

        if is_name_empty:
            raise EmptyFolderName(folder_name=name)

    def check_user_has_edit_access_folder_permission(
            self, folder_id: str, user_id: str):
        folder_permission_dto = self.folder_storage.get_user_folder_permission(
            folder_id=folder_id,
            user_id=user_id,
        )

        if not folder_permission_dto:
            raise UserNotFolderMember(user_id=user_id, folder_id=folder_id)

        is_not_full_edit = (
                folder_permission_dto.permission_type != PermissionType.FULL_EDIT
        )
        if is_not_full_edit:
            raise ModificationNotAllowed(user_id=user_id)
