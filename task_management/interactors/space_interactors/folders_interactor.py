from task_management.exceptions.custom_exceptions import InvalidOrderException
from task_management.exceptions.enums import PermissionsEnum, Visibility
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
        self.ensure_user_has_access_to_space(
            user_id=create_folder_data.created_by,
            space_id=create_folder_data.space_id,
            permission_storage=self.space_permission_storage
        )
        self.ensure_space_is_active(
            space_id=create_folder_data.space_id,
            space_storage=self.space_storage
        )

        result = self.folder_storage.create_folder(create_folder_data)
        self._create_folder_users_permissions(folder_id=result.folder_id,
                                              space_id=result.space_id,
                                              created_by=result.created_by)
        return result

    def update_folder(self, update_folder_data: UpdateFolderDTO,
                      user_id: str) -> FolderDTO:
        self.ensure_user_has_access_to_folder(
            user_id=user_id, folder_id=update_folder_data.folder_id,
            permission_storage=self.folder_permission_storage)
        self.ensure_folder_is_active(
            folder_id=update_folder_data.folder_id,
            folder_storage=self.folder_storage)
        folder_data = self.folder_storage.get_folder(
            folder_id=update_folder_data.folder_id)

        self.ensure_space_is_active(
            space_id=folder_data.space_id,
            space_storage=self.space_storage
        )

        return self.folder_storage.update_folder(update_folder_data)

    def reorder_folder(self, space_id: str, folder_id: str, user_id: str,
                       order: int) -> FolderDTO:
        self.ensure_folder_is_active(folder_id=folder_id,
                                     folder_storage=self.folder_storage)
        self.ensure_user_has_access_to_folder(folder_id=folder_id,
                                              user_id=user_id,
                                              permission_storage=self.folder_permission_storage)
        self._validate_the_folder_order(space_id=space_id, order=order)

        return self.folder_storage.reorder_folder(folder_id=folder_id,
                                                  order=order)

    def remove_folder(self, folder_id: str, user_id: str) -> FolderDTO:
        self.ensure_user_has_access_to_folder(
            user_id=user_id, folder_id=folder_id,
            permission_storage=self.folder_permission_storage)
        self.ensure_folder_is_active(
            folder_id=folder_id, folder_storage=self.folder_storage)

        return self.folder_storage.remove_folder(folder_id)

    def set_folder_visibility(self, folder_id: str, user_id: str,
                              visibility: Visibility) -> FolderDTO:
        self.ensure_user_has_access_to_folder(
            folder_id=folder_id, user_id=user_id,
            permission_storage=self.folder_permission_storage)
        self.ensure_folder_is_active(folder_id=folder_id,
                                     folder_storage=self.folder_storage)

        if visibility == Visibility.PUBLIC:
            return self.folder_storage.set_folder_public(folder_id=folder_id)

        return self.folder_storage.set_folder_private(folder_id=folder_id)

    def get_space_folders(self, space_id: str) -> list[FolderDTO]:
        self.ensure_space_is_active(space_id=space_id,
                                    space_storage=self.space_storage)

        return self.folder_storage.get_space_folders(space_ids=[space_id])


    def get_user_folder_permission(self, folder_id: str,
                                   user_id: str) -> UserFolderPermissionDTO:
        self.ensure_user_has_access_to_folder(
            user_id=user_id,

            folder_id=folder_id,
            permission_storage=self.folder_permission_storage
        )

        self.ensure_folder_is_active(
            folder_id=folder_id,

            folder_storage=self.folder_storage
        )

        return self.folder_permission_storage.get_user_permission_for_folder(
            folder_id=folder_id, user_id=user_id)

    def get_folder_permissions(self, folder_id: str) -> list[
        UserFolderPermissionDTO]:
        self.ensure_folder_is_active(folder_id=folder_id,
                                     folder_storage=self.folder_storage)

        return self.folder_permission_storage.get_folder_permissions(
            folder_id=folder_id)

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

    def _validate_the_folder_order(self, space_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)
        lists_count = self.folder_storage.get_space_folder_count(
            space_id=space_id)

        if order > lists_count:
            raise InvalidOrderException(order=order)
