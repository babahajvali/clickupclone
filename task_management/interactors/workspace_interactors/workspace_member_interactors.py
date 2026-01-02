from task_management.exceptions.custom_exceptions import \
    NotAccessToModificationException, UnexpectedRoleFoundException
from task_management.exceptions.enums import PermissionsEnum, RoleEnum
from task_management.interactors.dtos import AddMemberToWorkspaceDTO, \
    WorkspaceMemberDTO
from task_management.interactors.storage_interface.space_permission_storage_interface import \
    SpacePermissionStorageInterface
from task_management.interactors.storage_interface.user_storage_interface import \
    UserStorageInterface
from task_management.interactors.storage_interface.workspace_member_storage_interface import \
    WorkspaceMemberStorageInterface
from task_management.interactors.storage_interface.workspace_storage_interface import \
    WorkspaceStorageInterface
from task_management.interactors.validation_mixin import ValidationMixin


class WorkspaceMemberInteractor(ValidationMixin):

    def __init__(self,
                 workspace_member_storage: WorkspaceMemberStorageInterface,
                 workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface,
                 permission_storage: SpacePermissionStorageInterface):
        self.workspace_member_storage = workspace_member_storage
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage
        self.permission_storage = permission_storage

    def add_member_to_workspace(self,
                                workspace_member_data: AddMemberToWorkspaceDTO) -> WorkspaceMemberDTO:
        self.validate_workspace_exist_and_status(
            workspace_id=workspace_member_data.workspace_id,
            workspace_storage=self.workspace_storage)
        self.validate_user_exist_and_status(
            user_id=workspace_member_data.user_id,
            user_storage=self.user_storage)
        self.validate_user_exist_and_status(
            user_id=workspace_member_data.added_by,
            user_storage=self.user_storage)
        self._validate_role(role=workspace_member_data.role.value)
        self.validate_user_owner_or_editor_access(
            user_id=workspace_member_data.added_by,
            workspace_id=workspace_member_data.workspace_id,
            workspace_storage=self.workspace_storage,
            workspace_member_storage=self.workspace_member_storage)

        return self.workspace_member_storage.add_member_to_workspace(
            workspace_member_data=workspace_member_data)

    def remove_member_from_workspace(self, user_id: str, workspace_id: str,
                                     removed_by: str) -> WorkspaceMemberDTO:
        self.validate_workspace_exist_and_status(workspace_id=workspace_id,
                                                 workspace_storage=self.workspace_storage)
        self.validate_user_exist_and_status(user_id=user_id,
                                            user_storage=self.user_storage)
        self.validate_user_owner_or_editor_access(user_id=user_id,
                                                  workspace_id=workspace_id,
                                                  workspace_storage=self.workspace_storage,
                                                  workspace_member_storage=self.workspace_member_storage)

        return self.workspace_member_storage.remove_member_from_workspace(
            workspace_id=workspace_id, user_id=user_id)

    def change_member_role(self, workspace_id: str, user_id: str,
                           role: PermissionsEnum,
                           changed_by: str) -> WorkspaceMemberDTO:
        self.validate_workspace_exist_and_status(workspace_id=workspace_id,
                                                 workspace_storage=self.workspace_storage)
        self.validate_user_exist_and_status(user_id=user_id,
                                            user_storage=self.user_storage)
        self.validate_user_owner_or_editor_access(user_id=changed_by,
                                                  workspace_id=workspace_id,
                                                  workspace_storage=self.workspace_storage,
                                                  workspace_member_storage=self.workspace_member_storage)
        self._validate_role(role=role.value)

        return self.workspace_member_storage.update_the_member_role(
            workspace_id=workspace_id, user_id=user_id, role=role)

    @staticmethod
    def _validate_role(role: str):
        existed_roles = [type.value for type in RoleEnum]

        if role not in existed_roles:
            raise UnexpectedRoleFoundException(role=role)
