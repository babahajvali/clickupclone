from task_management.exceptions.custom_exceptions import InvalidOrderException
from task_management.exceptions.enums import Permissions, Visibility, Role
from task_management.interactors.dtos import CreateFolderDTO, FolderDTO, \
    UpdateFolderDTO, UserFolderPermissionDTO, CreateUserFolderPermissionDTO
from task_management.interactors.storage_interfaces.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interfaces.folder_permission_storage_interface import \
    FolderPermissionStorageInterface
from task_management.interactors.storage_interfaces.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interfaces.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin
from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache


class FolderInteractor(ValidationMixin):

    def __init__(self, folder_storage: FolderStorageInterface,
                 folder_permission_storage: FolderPermissionStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 space_storage: SpaceStorageInterface):
        self.folder_storage = folder_storage
        self.folder_permission_storage = folder_permission_storage
        self.workspace_member_storage = workspace_member_storage
        self.space_storage = space_storage

    @invalidate_interactor_cache(cache_name="folders")
    def create_folder(self, create_folder_data: CreateFolderDTO) -> FolderDTO:
        self.validate_space_is_active(
            space_id=create_folder_data.space_id,
            space_storage=self.space_storage
        )
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=create_folder_data.space_id)
        self.validate_user_has_access_to_workspace(
            user_id=create_folder_data.created_by,
            workspace_id=workspace_id,
            workspace_member_storage=self.workspace_member_storage)

        result = self.folder_storage.create_folder(create_folder_data)
        if create_folder_data.is_private:
            self._add_users_in_folder_permission(folder_id=result.folder_id,
                                                 workspace_id=workspace_id,
                                                 created_by=result.created_by)
        else:
            user_permission = CreateUserFolderPermissionDTO(
                folder_id=result.folder_id,
                user_id=result.created_by,
                permission_type=Permissions.FULL_EDIT,
                added_by=result.created_by,
            )
            self.folder_permission_storage.create_folder_users_permissions(
                users_permission_data=[user_permission])
        return result

    @invalidate_interactor_cache(cache_name="folders")
    def update_folder(self, update_folder_data: UpdateFolderDTO,
                      user_id: str) -> FolderDTO:
        self.validate_folder_is_active(
            folder_id=update_folder_data.folder_id,
            folder_storage=self.folder_storage)
        space_id = self.folder_storage.get_folder_space_id(
            folder_id=update_folder_data.folder_id)

        self.validate_space_is_active(
            space_id=space_id,
            space_storage=self.space_storage
        )
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            user_id=user_id,
            workspace_id=workspace_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.folder_storage.update_folder(update_folder_data)

    @invalidate_interactor_cache(cache_name="folders")
    def reorder_folder(self, space_id: str, folder_id: str, user_id: str,
                       order: int) -> FolderDTO:
        self.validate_folder_is_active(folder_id=folder_id,
                                       folder_storage=self.folder_storage)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            user_id=user_id,
            workspace_id=workspace_id,
            workspace_member_storage=self.workspace_member_storage)
        self._validate_the_folder_order(space_id=space_id, order=order)

        return self.folder_storage.reorder_folder(folder_id=folder_id,
                                                  new_order=order)

    @invalidate_interactor_cache(cache_name="folders")
    def remove_folder(self, folder_id: str, user_id: str) -> FolderDTO:
        self.validate_folder_is_active(
            folder_id=folder_id, folder_storage=self.folder_storage)
        space_id = self.folder_storage.get_folder_space_id(folder_id=folder_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            user_id=user_id,
            workspace_id=workspace_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.folder_storage.remove_folder(folder_id)

    @invalidate_interactor_cache(cache_name="folders")
    def set_folder_visibility(self, folder_id: str, user_id: str,
                              visibility: Visibility) -> FolderDTO:
        self.validate_folder_is_active(folder_id=folder_id,
                                       folder_storage=self.folder_storage)
        space_id = self.folder_storage.get_folder_space_id(folder_id=folder_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            user_id=user_id,
            workspace_id=workspace_id,
            workspace_member_storage=self.workspace_member_storage)
        self._validate_visibility_type(visibility=visibility.value)
        if visibility == Visibility.PUBLIC:
            return self.folder_storage.set_folder_public(folder_id=folder_id)

        return self.folder_storage.set_folder_private(folder_id=folder_id)

    @interactor_cache(cache_name="folders", timeout=5 * 60)
    def get_space_folders(self, space_id: str) -> list[FolderDTO]:
        self.validate_space_is_active(space_id=space_id,
                                      space_storage=self.space_storage)

        return self.folder_storage.get_space_folders(space_ids=[space_id])

    def get_user_folder_permission(self, folder_id: str,
                                   user_id: str) -> UserFolderPermissionDTO:
        self.validate_user_has_access_to_folder(
            user_id=user_id, folder_id=folder_id,
            permission_storage=self.folder_permission_storage
        )
        self.validate_folder_is_active(
            folder_id=folder_id,
            folder_storage=self.folder_storage
        )

        return self.folder_permission_storage.get_user_permission_for_folder(
            folder_id=folder_id, user_id=user_id)

    def get_folder_permissions(self, folder_id: str) -> list[
        UserFolderPermissionDTO]:
        self.validate_folder_is_active(folder_id=folder_id,
                                       folder_storage=self.folder_storage)

        return self.folder_permission_storage.get_folder_permissions(
            folder_id=folder_id)

    def add_user_for_folder_permission(self,
                                       permission_data: CreateUserFolderPermissionDTO):
        self.validate_folder_is_active(folder_id=permission_data.folder_id,
                                       folder_storage=self.folder_storage)
        space_id = self.folder_storage.get_folder_space_id(
            folder_id=permission_data.folder_id)
        workspace_id = self.space_storage.get_space_workspace_id(
            space_id=space_id)
        self.validate_user_has_access_to_workspace(
            user_id=permission_data.added_by,
            workspace_id=workspace_id,
            workspace_member_storage=self.workspace_member_storage)

        return self.folder_permission_storage.create_folder_users_permissions(
            users_permission_data=[permission_data])[0]

    def _add_users_in_folder_permission(self, folder_id: str,
                                        workspace_id: str,
                                        created_by: str) -> list[
        UserFolderPermissionDTO]:
        workspace_members_role = self.workspace_member_storage.get_workspace_members(
            workspace_id=workspace_id)
        folder_user_permissions = []

        for each in workspace_members_role:
            if each.role == Role.GUEST:
                user_permission = CreateUserFolderPermissionDTO(
                    folder_id=folder_id,
                    user_id=each.user_id,
                    permission_type=Permissions.VIEW,
                    added_by=created_by,
                )
            else:
                user_permission = CreateUserFolderPermissionDTO(
                    folder_id=folder_id,
                    user_id=each.user_id,
                    permission_type=Permissions.FULL_EDIT,
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
