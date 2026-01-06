from task_management.exceptions.custom_exceptions import InvalidOrderException
from task_management.exceptions.enums import PermissionsEnum, Role, Visibility
from task_management.interactors.dtos import CreateSpaceDTO, SpaceDTO, \
    UserSpacePermissionDTO, CreateUserSpacePermissionDTO, UpdateSpaceDTO
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
        self.ensure_user_can_modify_workspace(
            user_id=create_space_data.created_by,
            workspace_id=create_space_data.workspace_id,
            workspace_storage=self.workspace_storage,
            workspace_member_storage=self.workspace_member_storage)
        self.ensure_workspace_is_active(
            workspace_id=create_space_data.workspace_id,
            workspace_storage=self.workspace_storage)

        result = self.space_storage.create_space(
            create_space_data=create_space_data)

        self._create_space_users_permission(space_id=result.space_id,
                                            workspace_id=result.workspace_id,
                                            created_by=result.created_by)
        return result

    def update_space(self, update_space_data: UpdateSpaceDTO,
                     user_id: str) -> SpaceDTO:
        self.ensure_space_is_active(space_id=update_space_data.space_id,
                                    space_storage=self.space_storage)
        self.ensure_user_has_access_to_space(
            user_id=user_id, space_id=update_space_data.space_id,
            permission_storage=self.permission_storage)
        space_data = self.space_storage.get_space(
            space_id=update_space_data.space_id)
        self.ensure_workspace_is_active(
            workspace_id=space_data.workspace_id,
            workspace_storage=self.workspace_storage)

        return self.space_storage.update_space(
            update_space_data=update_space_data)

    def reorder_space(self, workspace_id: str, space_id: str, order: int,
                      user_id: str):
        self.ensure_user_has_access_to_space(
            space_id=space_id, user_id=user_id,
            permission_storage=self.permission_storage)
        self.ensure_workspace_is_active(
            workspace_id=workspace_id,
            workspace_storage=self.workspace_storage)
        self._validate_space_order(workspace_id=workspace_id, order=order)

    def delete_space(self, space_id: str, user_id: str) -> SpaceDTO:
        self.ensure_user_has_access_to_space(user_id=user_id,
                                             space_id=space_id,
                                             permission_storage=self.permission_storage)
        self.ensure_space_is_active(space_id=space_id,
                                    space_storage=self.space_storage)

        return self.space_storage.remove_space(space_id=space_id,
                                               user_id=user_id)

    def set_space_visibility(self, space_id: str, user_id: str,
                             visibility: Visibility):
        self.ensure_user_has_access_to_space(
            user_id=user_id, space_id=space_id,
            permission_storage=self.permission_storage)
        self.ensure_space_is_active(space_id=space_id,
                                    space_storage=self.space_storage)

        if visibility == Visibility.PUBLIC:
            return self.space_storage.set_space_public(space_id=space_id)

        return self.space_storage.set_space_private(space_id=space_id)

    def get_workspace_spaces(self, workspace_id: str) -> list[SpaceDTO]:
        self.ensure_workspace_is_active(workspace_id=workspace_id,
                                        workspace_storage=self.workspace_storage)

        return self.space_storage.get_workspace_spaces(
            workspace_id=workspace_id)

    # Permissions Section

    def get_space_permissions(self, space_id: str) -> list[
        UserSpacePermissionDTO]:
        self.ensure_space_is_active(
            space_id=space_id,
            space_storage=self.space_storage
        )

        return self.permission_storage.get_space_permissions(space_id=space_id)

    def _create_space_users_permission(self, workspace_id: str, space_id: str,
                                       created_by: str, ):
        workspace_members = self.workspace_member_storage.get_workspace_members(
            workspace_id=workspace_id)
        users_permissions = []
        for workspace_member in workspace_members:
            if workspace_member.role != Role.GUEST.value:
                user_permission = CreateUserSpacePermissionDTO(
                    space_id=space_id,
                    user_id=workspace_member.user_id,
                    permission_type=PermissionsEnum.FULL_EDIT,
                    is_active=True,
                    added_by=created_by
                )
            else:
                user_permission = CreateUserSpacePermissionDTO(
                    space_id=space_id,
                    user_id=workspace_member.user_id,
                    permission_type=PermissionsEnum.VIEW,
                    is_active=True,
                    added_by=created_by
                )
            users_permissions.append(user_permission)

        return self.permission_storage.create_user_space_permissions(
            permission_data=users_permissions)

    def _validate_space_order(self, workspace_id: str, order: int):
        if order < 1:
            raise InvalidOrderException(order=order)
        space_count = self.space_storage.get_workspace_spaces_count(
            workspace_id=workspace_id)

        if order > space_count:
            raise InvalidOrderException(order=order)
