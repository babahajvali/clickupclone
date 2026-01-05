from task_management.exceptions.custom_exceptions import \
    UserDoesNotHaveListPermissionException, InactiveUserPermissionException
from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import CreateListDTO, ListDTO, \
    UpdateListDTO, UserListPermissionDTO, CreateUserListPermissionDTO
from task_management.interactors.storage_interface.folder_permission_storage_interface import \
    FolderPermissionStorageInterface
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.list_permission_storage_interface import \
    ListPermissionStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.task_storage_interface import \
    TaskStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class ListInteractor(ValidationMixin):

    def __init__(self, list_storage: ListStorageInterface,
                 task_storage: TaskStorageInterface,
                 folder_storage: FolderStorageInterface,
                 space_storage: SpaceStorageInterface,
                 list_permission_storage: ListPermissionStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface,
                 space_permission_storage: SpacePermissionStorageInterface):
        self.list_storage = list_storage
        self.task_storage = task_storage
        self.folder_storage = folder_storage
        self.space_storage = space_storage
        self.list_permission_storage = list_permission_storage
        self.folder_permission_storage = folder_permission_storage
        self.space_permission_storage = space_permission_storage

    def create_list(self, create_list_data: CreateListDTO) -> ListDTO:
        if create_list_data.folder_id is not None:
            self.check_user_has_access_to_folder_modification(
                user_id=create_list_data.created_by,
                folder_id=create_list_data.folder_id,
                permission_storage=self.folder_permission_storage
            )
            self.validate_folder_exist_and_status(
                folder_id=create_list_data.folder_id,
                folder_storage=self.folder_storage
            )
            self.validate_list_order_in_folder(
                order=create_list_data.order,
                folder_id=create_list_data.folder_id,
                list_storage=self.list_storage
            )
        else:
            self.check_user_has_access_to_space_modification(
                user_id=create_list_data.created_by,
                space_id=create_list_data.space_id,
                permission_storage=self.space_permission_storage
            )
            self.validate_list_order_in_space(
                space_id=create_list_data.space_id,
                order=create_list_data.order,
                list_storage=self.list_storage
            )

        self.validate_space_exist_and_status(
            space_id=create_list_data.space_id,
            space_storage=self.space_storage
        )

        return self.list_storage.create_list(create_list_data=create_list_data)

    def update_list(self, update_list_data: UpdateListDTO) -> ListDTO:

        self.check_user_has_access_to_list_modification(
            user_id=update_list_data.created_by,
            list_id=update_list_data.list_id,
            permission_storage=self.list_permission_storage
        )

        self.check_list_exists_and_status(
            list_id=update_list_data.list_id,
            list_storage=self.list_storage
        )

        if update_list_data.folder_id is not None:
            self.validate_folder_exist_and_status(
                folder_id=update_list_data.folder_id,
                folder_storage=self.folder_storage
            )
            self.validate_list_order_in_folder(
                order=update_list_data.order,
                folder_id=update_list_data.folder_id,
                list_storage=self.list_storage
            )
        else:
            self.validate_space_exist_and_status(
                space_id=update_list_data.space_id,
                space_storage=self.space_storage
            )
            self.validate_list_order_in_space(
                space_id=update_list_data.space_id,
                order=update_list_data.order,
                list_storage=self.list_storage
            )

        return self.list_storage.update_list(update_list_data=update_list_data)

    def remove_list(self, list_id: str, user_id: str):
        self.check_user_has_access_to_list_modification(
            user_id=user_id,
            list_id=list_id,
            permission_storage=self.list_permission_storage
        )
        self.check_list_exists_and_status(
            list_id=list_id,
            list_storage=self.list_storage
        )

        return self.list_storage.remove_list(list_id=list_id)

    def set_list_private(self, list_id: str, user_id: str):
        self.check_user_has_access_to_list_modification(
            user_id=user_id,
            list_id=list_id,
            permission_storage=self.list_permission_storage
        )
        self.check_list_exists_and_status(
            list_id=list_id,
            list_storage=self.list_storage
        )

        return self.list_storage.make_list_private(list_id=list_id)

    def set_list_public(self, list_id: str, user_id: str):
        self.check_user_has_access_to_list_modification(
            user_id=user_id,
            list_id=list_id,
            permission_storage=self.list_permission_storage
        )
        self.check_list_exists_and_status(
            list_id=list_id,
            list_storage=self.list_storage
        )

        return self.list_storage.make_list_public(list_id=list_id)

    # Permission section

    def add_user_list_permission(self, list_id: str, user_id: str,
                                 added_by: str,
                                 permission_type: PermissionsEnum) -> UserListPermissionDTO:
        self.check_user_has_access_to_list_modification(
            user_id=added_by,
            list_id=list_id,
            permission_storage=self.list_permission_storage
        )
        self.check_list_exists_and_status(
            list_id=list_id,
            list_storage=self.list_storage
        )

        return self.list_permission_storage.add_user_permission_for_list(
            list_id=list_id,
            user_id=user_id,
            permission_type=permission_type
        )

    def change_user_list_permissions(self, user_id: str, list_id: str,
                                     changed_by: str,
                                     permission_type: PermissionsEnum) -> UserListPermissionDTO:
        self.check_user_has_access_to_list_modification(
            user_id=changed_by,
            list_id=list_id,
            permission_storage=self.list_permission_storage
        )
        self.check_list_exists_and_status(
            list_id=list_id,
            list_storage=self.list_storage
        )

        return self.list_permission_storage.update_user_permission_for_list(
            list_id=list_id,
            user_id=user_id,
            permission_type=permission_type
        )

    def remove_user_list_permission(self, list_id: str, user_id: str,
                                    removed_by: str) -> UserListPermissionDTO:
        self.check_list_exists_and_status(
            list_id=list_id, list_storage=self.list_storage)
        self._check_user_list_permission(list_id=list_id, user_id=user_id)
        self.check_user_has_access_to_list_modification(
            user_id=removed_by, list_id=list_id,
            permission_storage=self.list_permission_storage)

        return self.list_permission_storage.remove_user_permission_for_list(
            list_id=list_id, user_id=user_id)

    def get_list_permissions(self, list_id: str) -> list[
        UserListPermissionDTO]:
        self.check_list_exists_and_status(list_id=list_id,
                                          list_storage=self.list_storage)

        return self.list_permission_storage.get_list_permissions(
            list_id=list_id)

    def get_folder_lists(self, folder_id: str):
        self.validate_folder_exist_and_status(folder_id=folder_id,
                                              folder_storage=self.folder_storage)
        return self.list_storage.get_folder_lists(folder_ids=[folder_id])

    def get_space_lists(self, space_id: str):
        self.validate_space_exist_and_status(space_id=space_id,
                                             space_storage=self.space_storage)
        return self.list_storage.get_space_lists(space_ids=[space_id])

    # Helping functions

    def _check_user_list_permission(self, list_id: str, user_id: str):
        user_permission = self.list_permission_storage.get_user_permission_for_list(
            list_id=list_id, user_id=user_id)

        if not user_permission:
            raise UserDoesNotHaveListPermissionException(user_id=user_id)

        if not user_permission.is_active:
            raise InactiveUserPermissionException(user_id=user_id)

    def _create_list_users_permissions(self, list_id: str, space_id: str,
                                       created_by: str) -> list[
        UserListPermissionDTO]:
        space_user_permissions = self.space_permission_storage.get_space_permissions(
            space_id=space_id)
        list_user_permissions = []

        for each in space_user_permissions:
            if each.permission_type == PermissionsEnum.FULL_EDIT.value:
                user_permission = CreateUserListPermissionDTO(
                    list_id=list_id,
                    user_id=each.user_id,
                    permission_type=PermissionsEnum.FULL_EDIT,
                    is_active=True,
                    added_by=created_by,
                )
            elif each.permission_type == PermissionsEnum.COMMENT.value:
                user_permission = CreateUserListPermissionDTO(
                    list_id=list_id,
                    user_id=each.user_id,
                    permission_type=PermissionsEnum.COMMENT,
                    is_active=True,
                    added_by=created_by,
                )
            else:
                user_permission = CreateUserListPermissionDTO(
                    list_id=list_id,
                    user_id=each.user_id,
                    permission_type=PermissionsEnum.VIEW,
                    is_active=True,
                    added_by=created_by,
                )

            list_user_permissions.append(user_permission)

        return self.list_permission_storage.create_list_users_permissions(
            user_permissions=list_user_permissions)
