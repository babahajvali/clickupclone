from task_management.exceptions.enums import PermissionsEnum
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO
from task_management.interactors.storage_interface.folder_storage_interface import \
    FolderStorageInterface
from task_management.interactors.storage_interface.list_storage_interface import \
    ListStorageInterface
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.space_storage_interface import \
    SpaceStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class SpaceInteractor(ValidationMixin):

    def __init__(self, space_storage: SpaceStorageInterface,
                 folder_storage: FolderStorageInterface,
                 list_storage: ListStorageInterface,
                 permission_storage: SpacePermissionStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 workspace_member_storage: WorkspaceMemberStorageInterface):
        self.space_storage = space_storage
        self.folder_storage = folder_storage
        self.list_storage = list_storage
        self.permission_storage = permission_storage
        self.workspace_storage = workspace_storage
        self.workspace_member_storage = workspace_member_storage

    def create_space(self, create_space_data: CreateSpaceDTO) -> SpaceDTO:
        self.validate_user_owner_or_editor_access(
            user_id=create_space_data.created_by,
            workspace_id=create_space_data.workspace_id,
            workspace_storage=self.workspace_storage,
            workspace_member_storage=self.workspace_member_storage)
        self.check_space_order_exist(order=create_space_data.order,
                                     workspace_id=create_space_data.workspace_id,
                                     space_storage=self.space_storage)
        self.validate_workspace_exist_and_status(
            workspace_id=create_space_data.workspace_id,
            workspace_storage=self.workspace_storage)

        return self.space_storage.create_space(
            create_space_data=create_space_data)

    def update_space(self, update_space_data: SpaceDTO) -> SpaceDTO:
        self.validate_space_exist_and_status(
            space_id=update_space_data.space_id,
            space_storage=self.space_storage)
        self.check_user_has_access_to_space_modification(
            user_id=update_space_data.created_by,
            space_id=update_space_data.space_id,
            permission_storage=self.permission_storage)
        self.check_space_order_exist(order=update_space_data.order,
                                     workspace_id=update_space_data.workspace_id,
                                     space_storage=self.space_storage)
        self.validate_workspace_exist_and_status(
            workspace_id=update_space_data.workspace_id,
            workspace_storage=self.workspace_storage)

        return self.space_storage.update_space(
            update_space_data=update_space_data)

    def delete_space(self, space_id: str, user_id: str) -> SpaceDTO:
        self.check_user_has_access_to_space_modification(
            user_id=user_id,
            space_id=space_id,
            permission_storage=self.permission_storage)
        self.validate_space_exist_and_status(space_id=space_id,
                                             space_storage=self.space_storage)

        return self.space_storage.remove_space(space_id=space_id,
                                               user_id=user_id)

    def set_space_private(self, space_id: str, user_id: str) -> SpaceDTO:
        self.check_user_has_access_to_space_modification(
            user_id=user_id,
            space_id=space_id,
            permission_storage=self.permission_storage)
        self.validate_space_exist_and_status(space_id=space_id,
                                             space_storage=self.space_storage)
        return self.space_storage.set_space_private(space_id=space_id,
                                                    user_id=user_id)

    def set_space_public(self, space_id: str, user_id: str) -> SpaceDTO:
        self.check_user_has_access_to_space_modification(
            user_id=user_id,
            space_id=space_id,
            permission_storage=self.permission_storage)
        self.validate_space_exist_and_status(space_id=space_id,
                                             space_storage=self.space_storage)

        return self.space_storage.set_space_public(space_id=space_id,
                                                   user_id=user_id)

    def get_workspace_spaces(self, workspace_id: str) -> list[SpaceDTO]:
        self.validate_workspace_exist_and_status(workspace_id=workspace_id,
                                                 workspace_storage=self.workspace_storage)

        return self.space_storage.get_workspace_spaces(
            workspace_id=workspace_id)

    # Permissions Section
    def add_space_permission(self, space_id: str, user_id: str, added_by: str,
                             permission_type: PermissionsEnum) :
        self.check_user_has_access_to_space_modification(
            user_id=added_by,
            space_id=space_id,
            permission_storage=self.permission_storage
        )

        # Validate space exists
        self.validate_space_exist_and_status(
            space_id=space_id,
            space_storage=self.space_storage
        )

        return self.permission_storage.add_user_permission_for_space(
            space_id=space_id,
            user_id=user_id,
            permission_type=permission_type
        )

    def change_space_permissions(self, space_id: str, user_id: str,
                                 changed_by: str,
                                 permission_type: PermissionsEnum) :
        self.check_user_has_access_to_space_modification(
            user_id=changed_by,
            space_id=space_id,
            permission_storage=self.permission_storage
        )

        # Validate space exists
        self.validate_space_exist_and_status(
            space_id=space_id,
            space_storage=self.space_storage
        )

        return self.permission_storage.update_user_permission_for_space(
            space_id=space_id,
            user_id=user_id,
            permission_type=permission_type
        )

    def remove_space_permission(self, space_id: str, user_id: str,
                                removed_by: str):
        self.check_user_has_access_to_space_modification(
            user_id=removed_by,
            space_id=space_id,
            permission_storage=self.permission_storage
        )

        self.validate_space_exist_and_status(
            space_id=space_id,
            space_storage=self.space_storage
        )

        return self.permission_storage.remove_user_permission_for_space(
            space_id=space_id,
            user_id=user_id
        )

    def get_space_permissions(self, space_id: str):
        self.validate_space_exist_and_status(
            space_id=space_id,
            space_storage=self.space_storage
        )

        return self.permission_storage.get_space_permissions(space_id=space_id)
