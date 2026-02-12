from task_management.exceptions.enums import Permissions, Role
from task_management.interactors.dtos import AddMemberToWorkspaceDTO, \
    WorkspaceMemberDTO

from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface,UserStorageInterface
from task_management.mixins import WorkspaceValidationMixin,UserValidationMixin


class WorkspaceMemberInteractor(WorkspaceValidationMixin, UserValidationMixin):

    def __init__(self,
                 workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface):
        super().__init__(workspace_storage=workspace_storage,
                         user_storage=workspace_storage)
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def add_member_to_workspace(self,
                                workspace_member_data: AddMemberToWorkspaceDTO) -> WorkspaceMemberDTO:
        existed_member = self.workspace_storage.get_workspace_member(
            workspace_id=workspace_member_data.workspace_id,
            user_id=workspace_member_data.user_id)
        if existed_member:
            if not existed_member.is_active:
                existed_member = self.workspace_storage.re_add_member_to_workspace(
                    workspace_member_data=workspace_member_data)
            return existed_member
        self.validate_workspace_is_active(
            workspace_id=workspace_member_data.workspace_id)
        self.validate_user_is_active(
            user_id=workspace_member_data.user_id)
        self.validate_role(role=workspace_member_data.role.value)

        self.validate_user_has_access_to_workspace(
            user_id=workspace_member_data.added_by,
            workspace_id=workspace_member_data.workspace_id)

        workspace_member = self.workspace_storage.add_member_to_workspace(
            workspace_member_data=workspace_member_data)

        return workspace_member

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def remove_member_from_workspace(self, workspace_member_id: int,
                                     removed_by: str) -> WorkspaceMemberDTO:
        self.validate_workspace_member_is_active(
            workspace_member_id=workspace_member_id)
        workspace_member_data = self.workspace_storage.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id)
        self.validate_user_has_access_to_workspace(
            user_id=removed_by,
            workspace_id=workspace_member_data.workspace_id)

        workspace_member = self.workspace_storage.remove_member_from_workspace(
            workspace_member_id=workspace_member_id)

        return workspace_member

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def change_member_role(self, workspace_id: str, user_id: str, role: str,
                           changed_by: str) -> WorkspaceMemberDTO:
        self.validate_workspace_is_active(workspace_id=workspace_id)
        self.validate_user_is_active(user_id=user_id)
        self.validate_user_permission_for_change_workspace_role(
            user_id=changed_by,
            workspace_id=workspace_id)
        self.validate_role(role=role)

        workspace_member = self.workspace_storage.update_the_member_role(
            workspace_id=workspace_id, user_id=user_id, role=role)

        return workspace_member

    @interactor_cache(cache_name="user_workspaces", timeout=5 * 60)
    def get_user_workspaces(self, user_id: str) -> list[WorkspaceMemberDTO]:

        return self.workspace_storage.get_user_workspaces(
            user_id=user_id)

    @staticmethod
    def _get_permission_type_by_role(role: str) -> Permissions:
        if role == Role.GUEST.value:
            return Permissions.VIEW
        else:
            return Permissions.FULL_EDIT

    @staticmethod
    def validate_role(role: str):
        existed_roles = Role.get_values()
        if role not in existed_roles:
            from task_management.exceptions.custom_exceptions import \
                UnexpectedRoleException
            raise UnexpectedRoleException(role=role)
