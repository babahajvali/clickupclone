from task_management.exceptions.custom_exceptions import \
    UserDoesNotHaveFolderPermissionException, InactiveUserPermissionException
from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    UpdateFolderDTO, UserFolderPermissionDTO, CreateUserFolderPermissionDTO
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.folder_permission_storage_interface import \
    FolderPermissionStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class FolderInteractor(ValidationMixin):

    def __init__(self, folder_storage: FolderStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface,
                 space_storage: SpaceStorageInterface):
        self.folder_storage = folder_storage
        self.folder_permission_storage = folder_permission_storage
        self.space_permission_storage = space_permission_storage
        self.space_storage = space_storage

    def create_folder(self, create_folder_data: CreateFolderDTO) -> FolderDTO:
        self.check_user_has_access_to_space_modification(
            user_id=create_folder_data.created_by,
            space_id=create_folder_data.space_id,
            permission_storage=self.space_permission_storage
        )

        self.validate_space_exist_and_status(
            space_id=create_folder_data.space_id,
            space_storage=self.space_storage
        )

        self.validate_folder_order(
            order=create_folder_data.order,
            space_id=create_folder_data.space_id,
            folder_storage=self.folder_storage
        )

        return self.folder_storage.create_folder(create_folder_data)

    def update_folder(self, update_folder_data: UpdateFolderDTO) -> FolderDTO:
        self.check_user_has_access_to_folder_modification(
            user_id=update_folder_data.created_by,
            folder_id=update_folder_data.folder_id,
            permission_storage=self.folder_permission_storage
        )

        self.validate_folder_exist_and_status(
            folder_id=update_folder_data.folder_id,
            folder_storage=self.folder_storage
        )

        self.validate_space_exist_and_status(
            space_id=update_folder_data.space_id,
            space_storage=self.space_storage
        )

        self.validate_folder_order(
            order=update_folder_data.order,
            space_id=update_folder_data.space_id,
            folder_storage=self.folder_storage
        )

        return self.folder_storage.update_folder(update_folder_data)

    def remove_folder(self, folder_id: str, user_id: str) -> FolderDTO:
        self.check_user_has_access_to_folder_modification(
            user_id=user_id,
            folder_id=folder_id,
            permission_storage=self.folder_permission_storage
        )

        self.validate_folder_exist_and_status(
            folder_id=folder_id,
            folder_storage=self.folder_storage
        )

        return self.folder_storage.remove_folder(folder_id)

    def make_folder_private(self, folder_id: str, user_id: str) -> FolderDTO:
        self.check_user_has_access_to_folder_modification(
            user_id=user_id,
            folder_id=folder_id,
            permission_storage=self.folder_permission_storage
        )

        self.validate_folder_exist_and_status(
            folder_id=folder_id,
            folder_storage=self.folder_storage
        )

        return self.folder_storage.set_folder_private(folder_id=folder_id)

    def make_folder_public(self, folder_id: str, user_id: str) -> FolderDTO:
        self.check_user_has_access_to_folder_modification(
            user_id=user_id,
            folder_id=folder_id,
            permission_storage=self.folder_permission_storage
        )

        self.validate_folder_exist_and_status(
            folder_id=folder_id,
            folder_storage=self.folder_storage
        )

        return self.folder_storage.set_folder_public(folder_id=folder_id)

    def get_space_folders(self, space_id: str) -> list[FolderDTO]:
        self.validate_space_exist_and_status(
            space_id=space_id,
            space_storage=self.space_storage
        )

        return self.folder_storage.get_space_folders(space_ids=[space_id])

    def add_user_folder_permission(self, folder_id: str, user_id: str,
                                   added_by: str,
                                   permission_type: PermissionsEnum) -> UserFolderPermissionDTO:
        self.check_user_has_access_to_folder_modification(
            user_id=added_by,
            folder_id=folder_id,
            permission_storage=self.folder_permission_storage
        )

        self.validate_folder_exist_and_status(
            folder_id=folder_id,
            folder_storage=self.folder_storage
        )

        return self.folder_permission_storage.add_user_permission_for_folder(
            folder_id=folder_id,
            user_id=user_id,
            permission_type=permission_type
        )

    def change_user_folder_permissions(self, folder_id: str, user_id: str,
                                       changed_by: str,
                                       permission_type: PermissionsEnum) -> UserFolderPermissionDTO:
        self._check_user_have_folder_permission(folder_id=folder_id,user_id=user_id)
        self.check_user_has_access_to_folder_modification(
            user_id=changed_by,
            folder_id=folder_id,
            permission_storage=self.folder_permission_storage
        )

        self.validate_folder_exist_and_status(
            folder_id=folder_id,
            folder_storage=self.folder_storage
        )

        return self.folder_permission_storage.update_user_permission_for_folder(
            folder_id=folder_id,
            user_id=user_id,
            permission_type=permission_type
        )

    def remove_user_folder_permission(self, folder_id: str, user_id: str,
                                      removed_by: str) -> UserFolderPermissionDTO:
        self.check_user_has_access_to_folder_modification(
            user_id=removed_by,
            folder_id=folder_id,
            permission_storage=self.folder_permission_storage
        )
        self._check_user_have_folder_permission(folder_id=folder_id, user_id=user_id)

        # Validate folder exists
        self.validate_folder_exist_and_status(
            folder_id=folder_id,
            folder_storage=self.folder_storage
        )

        return self.folder_permission_storage.remove_user_permission_for_folder(
            folder_id=folder_id,
            user_id=user_id
        )

    def get_user_folder_permission(self, folder_id: str,
                                   user_id: str) -> UserFolderPermissionDTO:
        self.check_user_has_access_to_folder_modification(
            user_id=user_id,

            folder_id=folder_id,
            permission_storage=self.folder_permission_storage
        )

        self.validate_folder_exist_and_status(
            folder_id=folder_id,

            folder_storage=self.folder_storage
        )

        return self.folder_permission_storage.get_user_permission_for_folder(
            folder_id=folder_id, user_id=user_id)

    def get_folder_permissions(self, folder_id: str) -> list[
        UserFolderPermissionDTO]:
        self.validate_folder_exist_and_status(folder_id=folder_id,
                                              folder_storage=self.folder_storage)

        return self.folder_permission_storage.get_folder_permissions(
            folder_id=folder_id)

    def _check_user_have_folder_permission(self, folder_id: str, user_id: str):
        user_permission = self.folder_permission_storage.get_user_permission_for_folder(
            user_id=user_id, folder_id=folder_id)

        if not user_permission:
            raise UserDoesNotHaveFolderPermissionException(user_id=user_id)

        if not user_permission.is_active:
            raise InactiveUserPermissionException(user_id=user_id)

    def _create_folder_users_permissions(self, folder_id: str, space_id: str,
                                         created_by: str) -> list[
        UserFolderPermissionDTO]:
        space_user_permissions = self.space_permission_storage.get_space_permissions(
            space_id=space_id)
        folder_user_permissions = []

        for each in space_user_permissions:
            if each.permission_type == PermissionsEnum.FULL_EDIT.value:
                user_permission = CreateUserFolderPermissionDTO(
                    folder_id=folder_id,
                    user_id=each.user_id,
                    permission_type=PermissionsEnum.FULL_EDIT,
                    is_active=True,
                    added_by=created_by,
                )
            elif each.permission_type == PermissionsEnum.COMMENT.value:
                user_permission = CreateUserFolderPermissionDTO(
                    folder_id=folder_id,
                    user_id=each.user_id,
                    permission_type=PermissionsEnum.COMMENT,
                    is_active=True,
                    added_by=created_by,
                )
            else:
                user_permission = CreateUserFolderPermissionDTO(
                    folder_id=folder_id,
                    user_id=each.user_id,
                    permission_type=PermissionsEnum.VIEW,
                    is_active=True,
                    added_by=created_by,
                )

            folder_user_permissions.append(user_permission)

        return self.folder_permission_storage.create_folder_users_permissions(
            users_permission_data=folder_user_permissions)
