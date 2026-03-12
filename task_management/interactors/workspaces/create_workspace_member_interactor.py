from task_management.decorators.caching_decorators import \
    invalidate_interactor_cache
from task_management.interactors.dtos import WorkspaceMemberDTO, \
    CreateWorkspaceMemberDTO
from task_management.interactors.storage_interfaces import \
    WorkspaceStorageInterface, UserStorageInterface
from task_management.mixins import WorkspaceValidationMixin, \
    UserValidationMixin


class CreateWorkspaceMemberInteractor(
    WorkspaceValidationMixin,
    UserValidationMixin):

    def __init__(
            self, workspace_storage: WorkspaceStorageInterface,
            user_storage: UserStorageInterface):
        super().__init__(
            workspace_storage=workspace_storage,
            user_storage=user_storage,
        )
        self.workspace_storage = workspace_storage
        self.user_storage = user_storage

    @invalidate_interactor_cache(cache_name="user_workspaces")
    @invalidate_interactor_cache(cache_name="validate_permission")
    def create_workspace_member(
            self, add_workspace_member_dto: CreateWorkspaceMemberDTO) \
            -> WorkspaceMemberDTO:
        self.check_role(role=add_workspace_member_dto.role.value)
        self.check_user_is_active(user_id=add_workspace_member_dto.user_id)
        self.check_workspace_not_deleted(
            workspace_id=add_workspace_member_dto.workspace_id
        )
        self.check_user_has_edit_access_to_workspace(
            user_id=add_workspace_member_dto.added_by,
            workspace_id=add_workspace_member_dto.workspace_id,
        )

        return self.workspace_storage.create_workspace_member(
            workspace_member_dto=add_workspace_member_dto
        )
