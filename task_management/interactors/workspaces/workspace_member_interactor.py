from task_management.interactors.dtos import AddMemberToWorkspaceDTO, \
    WorkspaceMemberDTO

from task_management.decorators.caching_decorators import interactor_cache, \
    invalidate_interactor_cache
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface
from task_management.interactors.workspaces.validators.workspace_validator import \
    WorkspaceValidator
from task_management.mixins import WorkspaceValidationMixin, \
    UserValidationMixin


class WorkspaceMemberInteractor:

    def __init__(self,
                 workspace_storage: WorkspaceStorageInterface,
                 user_storage: UserStorageInterface):
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage

    @property
    def workspace_mixin(self) -> WorkspaceValidationMixin:
        return WorkspaceValidationMixin(
            workspace_storage=self.workspace_storage)

    @property
    def user_mixin(self) -> UserValidationMixin:
        return UserValidationMixin(user_storage=self.user_storage)

    @property
    def workspace_validator(self) -> WorkspaceValidator:
        return WorkspaceValidator(workspace_storage=self.workspace_storage)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def add_member_to_workspace(
            self, workspace_member_data: AddMemberToWorkspaceDTO) \
            -> WorkspaceMemberDTO:
        self.workspace_mixin.check_workspace_is_active(
            workspace_id=workspace_member_data.workspace_id)
        self.user_mixin.check_user_is_active(
            user_id=workspace_member_data.user_id)
        self.workspace_mixin.check_user_has_access_to_workspace(
            user_id=workspace_member_data.added_by,
            workspace_id=workspace_member_data.workspace_id)
        self.workspace_validator.check_role(
            role=workspace_member_data.role.value)

        return self.workspace_storage.add_member_to_workspace(
            workspace_member_data=workspace_member_data)

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def remove_member_from_workspace(self, workspace_member_id: int,
                                     removed_by: str) -> WorkspaceMemberDTO:
        self.workspace_validator.check_workspace_member_is_active_by_id(
            workspace_member_id=workspace_member_id)
        workspace_member_data = self.workspace_storage.get_workspace_member_by_id(
            workspace_member_id=workspace_member_id)

        self.workspace_mixin.check_user_has_access_to_workspace(
            user_id=removed_by,
            workspace_id=workspace_member_data.workspace_id)

        workspace_member = self.workspace_storage.remove_member_from_workspace(
            workspace_member_id=workspace_member_id)

        return workspace_member

    @invalidate_interactor_cache(cache_name="user_workspaces")
    def change_member_role(self, workspace_id: str, user_id: str, role: str,
                           changed_by: str) -> WorkspaceMemberDTO:
        self.workspace_mixin.check_workspace_is_active(
            workspace_id=workspace_id)
        self.user_mixin.check_user_is_active(user_id=user_id)
        self.workspace_validator.check_workspace_member_is_active(
            workspace_id=workspace_id, user_id=user_id)
        (self.workspace_validator.
        check_user_permission_for_change_workspace_role(
            user_id=changed_by, workspace_id=workspace_id))
        self.workspace_validator.check_role(role=role)

        workspace_member = self.workspace_storage.update_the_member_role(
            workspace_id=workspace_id, user_id=user_id, role=role)

        return workspace_member

    @interactor_cache(cache_name="user_workspaces", timeout=5 * 60)
    def get_user_workspaces(self, user_id: str) -> list[WorkspaceMemberDTO]:
        self.user_mixin.check_user_is_active(user_id=user_id)

        return self.workspace_storage.get_active_user_workspaces(
            user_id=user_id)
