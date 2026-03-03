from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import WorkspaceMemberDTO, \
    AddMemberToWorkspaceDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface
from task_management.interactors.workspaces.validators.workspace_validator import \
    WorkspaceValidator
from task_management.mixins import WorkspaceValidationMixin, \
    UserValidationMixin


class AddWorkspaceMemberInteractor:

    def __init__(
            self, workspace_storage: WorkspaceStorageInterface,
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
        self.workspace_validator.check_role(
            role=workspace_member_data.role.value
        )
        self.workspace_mixin.check_workspace_not_deleted(
            workspace_id=workspace_member_data.workspace_id
        )
        self.user_mixin.check_user_is_active(
            user_id=workspace_member_data.user_id
        )
        self.workspace_mixin.check_user_has_edit_access_to_workspace(
            user_id=workspace_member_data.added_by,
            workspace_id=workspace_member_data.workspace_id
        )

        return self.workspace_storage.add_member_to_workspace(
            workspace_member_data=workspace_member_data
        )
